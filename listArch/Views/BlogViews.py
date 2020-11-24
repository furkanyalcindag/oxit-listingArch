from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import redirect, render
from listArch.Forms.BlogDescForm import BlogDescForm
from listArch.Forms.BlogDescImageForm import BlogDescImageForm
from listArch.Forms.CompanyBlogForm import CompanyBlogForm

from listArch.models import Company, Image, BlogImage, BlogDesc, Blog, Product, BlogProduct, ProfileBlog, BusinessType, \
    Profile
from listArch.models.CompanyBlog import CompanyBlog
from listArch.services import general_methods


def add_blog_desc(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    blogDesc_form = BlogDescForm()
    blogDesc_image_form = BlogDescImageForm()
    company_blog_form = CompanyBlogForm()
    companies = Company.objects.all()
    try:
        if request.method == 'POST':
            blogDesc_form = BlogDescForm(request.POST or None)
            blogDesc_image_form = BlogDescImageForm(request.POST, request.FILES or None)
            company_blog_form = CompanyBlogForm(request.POST or None)

            if blogDesc_image_form.is_valid() and company_blog_form.is_valid():

                blog = Blog(key=request.POST['title[tr]'])
                blog.save()

                blog_desc = BlogDesc(blog=blog, description=request.POST['content[eng]'],
                                     title_desc=request.POST['title[eng]'],
                                     lang_code=2)
                blog_desc.save()

                blog_desc2 = BlogDesc(blog=blog, description=request.POST['content[tr]'],
                                      title_desc=request.POST['title[tr]'],
                                      lang_code=1)
                blog_desc2.save()

                image_row = int(request.POST['image_row'])
                i = 0
                while i <= image_row:
                    image = Image(image=blogDesc_image_form.files['product_image[' + str(i) + '][image]'])
                    image.save()
                    blog_image = BlogImage(blog=blog, image=image)
                    blog_image.save()
                    i = i + 1

                blog_company = CompanyBlog(blog=blog, product=Product.objects.get(pk=int(request.POST['product'])),
                                           company=Company.objects.get(pk=int(request.POST['company_id'])))
                blog_company.save()

                messages.success(request, "Blog Bilgileri Başarıyla Kayıt Edildi.")
                return redirect('listArch:blog-ekle')
            else:
                messages.success(request, "Alanları kontrol ediniz.")

    except Exception as e:
        print(e)
        return redirect('listArch:admin-error-sayfasi')
    return render(request, 'blog/add-blog.html',
                  {'blogDesc_form': blogDesc_form, 'companies': companies, 'company_blog_form': company_blog_form})


def update_blog(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    blog = Blog.objects.get(pk=pk)

    blog_tr = BlogDesc.objects.filter(lang_code=1).filter(blog=blog)[0]
    blog_eng = BlogDesc.objects.filter(lang_code=2).filter(blog=blog)[0]
    images_blog = BlogImage.objects.filter(blog=blog)
    company_blog = CompanyBlog.objects.filter(blog=blog)
    product_blog = company_blog.product
    companies = Company.objects.all()
    products = Product.objects.all()

    company_blog_form = CompanyBlogForm(request.POST or None, request.FILES or None, instance=company_blog[0])

    try:
        if request.method == 'POST':
            if company_blog_form.is_valid():

                blog.key = request.POST['content[tr]']
                blog.save()

                blog_tr.description = request.POST['content[tr]']
                blog_tr.title_desc = request.POST['title[tr]']
                blog_tr.save()

                blog_eng.description = request.POST['content[eng]']
                blog_eng.title_desc = request.POST['title[eng]']
                blog_eng.save()

                for f in request.FILES.getlist('input2[]'):
                    image = Image(image=f)
                    image.save()
                    blog_image = BlogImage(image=image, blog=blog)
                    blog_image.save()

                for company_blog in company_blog:
                    company_blog.product = company_blog_form.cleaned_data['product']
                    company_blog.save()
                    company_blog.company = Company.objects.get(pk=int(request.POST['company_id']))
                    company_blog.save()

                messages.success(request, "Blog Bilgileri Başarıyla Düzenlendi.")
                return redirect('listArch:bloglar')

    except Exception as e:
        print(e)
        return redirect('listArch:admin-error-sayfasi')
    return render(request, 'blog/update-blog.html',
                  {'companies': companies, 'images': images_blog, 'blog': blog, 'product_blog': product_blog,
                   'blog_tr': blog_tr, 'blog_eng': blog_eng, 'company_blog': company_blog,
                   'company_blog_form': company_blog_form, 'products': products})


def blogs(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    blogs = BlogDesc.objects.filter(lang_code=1)
    array = []
    for blog in blogs:
        dict_blog = dict()
        dict_blog['images'] = BlogImage.objects.filter(blog=blog.blog)
        dict_blog['blog'] = blog
        dict_blog['desc'] = BlogDesc.objects.filter(blog=blog.blog)
        array.append(dict_blog)

    return render(request, 'blog/blogs.html', {'blogs': blogs})


def delete_blog(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            blog_id = request.POST['blog_id']
            blog = Blog.objects.get(pk=blog_id)
            blog.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


def add_blog_businessType(request, pk):
    blogDesc_image_form = BlogDescImageForm()
    profile = Profile.objects.get(pk=pk)
    if request.method == 'POST':
        try:

            blogDesc_image_form = BlogDescImageForm(request.POST, request.FILES)

            if blogDesc_image_form.is_valid():

                blog = Blog(key=request.POST['title[tr]'])
                blog.save()

                blog_desc = BlogDesc(blog=blog, description=request.POST['content[eng]'],
                                     title_desc=request.POST['title[eng]'],
                                     lang_code=2)
                blog_desc.save()

                blog_desc2 = BlogDesc(blog=blog, description=request.POST['content[tr]'],
                                      title_desc=request.POST['title[tr]'],
                                      lang_code=1)
                blog_desc2.save()

                image_row = int(request.POST['image_row'])
                i = 0
                while i <= image_row:
                    image = Image(image=blogDesc_image_form.files['product_image[' + str(i) + '][image]'])
                    image.save()
                    blog_image = BlogImage(blog=blog, image=image)
                    blog_image.save()
                    i = i + 1

                blog_business = ProfileBlog(profile=profile, blog=blog)
                blog_business.save()

                messages.success(request, "Blog Bilgileri Başarıyla Kayıt Edildi.")
                return redirect('listArch:profil-listesi')
            else:
                messages.success(request, "Alanları kontrol ediniz.")

        except Exception as e:
            print(e)
            return redirect('listArch:admin-error-sayfasi')
    else:
        return render(request, 'blog/add_businessType_blog.html', {'profile': profile})
