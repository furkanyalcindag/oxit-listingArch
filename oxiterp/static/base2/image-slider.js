/*!
Jssor Slider (MIT license)
*/
/* eslint-disable */
!function (i, h, m, e, d, k, f) {
    new (function () {
    });
    var c = {
        u: m.PI,
        l: m.max,
        j: m.min,
        H: m.ceil,
        G: m.floor,
        P: m.abs,
        gb: m.sin,
        Cb: m.cos,
        Oe: m.tan,
        Xf: m.atan,
        Yf: m.atan2,
        xb: m.sqrt,
        B: m.pow,
        dd: m.random,
        $Round: m.round,
        Y: function (d, b) {
            var a = c.B(10, b || 0);
            return c.$Round(d * a) / a
        }
    };

    function r(a) {
        return function (b) {
            return c.$Round(b * a) / a
        }
    }

    var g = i.$Jease$ = {
        $Swing: function (a) {
            return -c.Cb(a * c.u) / 2 + .5
        }, $Linear: function (a) {
            return a
        }, $InQuad: function (a) {
            return a * a
        }, $OutQuad: function (a) {
            return -a * (a - 2)
        }, $InOutQuad: function (a) {
            return (a *= 2) < 1 ? 1 / 2 * a * a : -1 / 2 * (--a * (a - 2) - 1)
        }, $InCubic: function (a) {
            return a * a * a
        }, $OutCubic: function (a) {
            return (a -= 1) * a * a + 1
        }, $InOutCubic: function (a) {
            return (a *= 2) < 1 ? 1 / 2 * a * a * a : 1 / 2 * ((a -= 2) * a * a + 2)
        }, $InQuart: function (a) {
            return a * a * a * a
        }, $OutQuart: function (a) {
            return -((a -= 1) * a * a * a - 1)
        }, $InOutQuart: function (a) {
            return (a *= 2) < 1 ? 1 / 2 * a * a * a * a : -1 / 2 * ((a -= 2) * a * a * a - 2)
        }, $InQuint: function (a) {
            return a * a * a * a * a
        }, $OutQuint: function (a) {
            return (a -= 1) * a * a * a * a + 1
        }, $InOutQuint: function (a) {
            return (a *= 2) < 1 ? 1 / 2 * a * a * a * a * a : 1 / 2 * ((a -= 2) * a * a * a * a + 2)
        }, $InSine: function (a) {
            return 1 - c.Cb(c.u / 2 * a)
        }, $OutSine: function (a) {
            return c.gb(c.u / 2 * a)
        }, $InOutSine: function (a) {
            return -1 / 2 * (c.Cb(c.u * a) - 1)
        }, $InExpo: function (a) {
            return a == 0 ? 0 : c.B(2, 10 * (a - 1))
        }, $OutExpo: function (a) {
            return a == 1 ? 1 : -c.B(2, -10 * a) + 1
        }, $InOutExpo: function (a) {
            return a == 0 || a == 1 ? a : (a *= 2) < 1 ? 1 / 2 * c.B(2, 10 * (a - 1)) : 1 / 2 * (-c.B(2, -10 * --a) + 2)
        }, $InCirc: function (a) {
            return -(c.xb(1 - a * a) - 1)
        }, $OutCirc: function (a) {
            return c.xb(1 - (a -= 1) * a)
        }, $InOutCirc: function (a) {
            return (a *= 2) < 1 ? -1 / 2 * (c.xb(1 - a * a) - 1) : 1 / 2 * (c.xb(1 - (a -= 2) * a) + 1)
        }, $InElastic: function (a) {
            if (!a || a == 1) return a;
            var b = .3, d = .075;
            return -(c.B(2, 10 * (a -= 1)) * c.gb((a - d) * 2 * c.u / b))
        }, $OutElastic: function (a) {
            if (!a || a == 1) return a;
            var b = .3, d = .075;
            return c.B(2, -10 * a) * c.gb((a - d) * 2 * c.u / b) + 1
        }, $InOutElastic: function (a) {
            if (!a || a == 1) return a;
            var b = .45, d = .1125;
            return (a *= 2) < 1 ? -.5 * c.B(2, 10 * (a -= 1)) * c.gb((a - d) * 2 * c.u / b) : c.B(2, -10 * (a -= 1)) * c.gb((a - d) * 2 * c.u / b) * .5 + 1
        }, $InBack: function (a) {
            var b = 1.70158;
            return a * a * ((b + 1) * a - b)
        }, $OutBack: function (a) {
            var b = 1.70158;
            return (a -= 1) * a * ((b + 1) * a + b) + 1
        }, $InOutBack: function (a) {
            var b = 1.70158;
            return (a *= 2) < 1 ? 1 / 2 * a * a * (((b *= 1.525) + 1) * a - b) : 1 / 2 * ((a -= 2) * a * (((b *= 1.525) + 1) * a + b) + 2)
        }, $InBounce: function (a) {
            return 1 - g.$OutBounce(1 - a)
        }, $OutBounce: function (a) {
            return a < 1 / 2.75 ? 7.5625 * a * a : a < 2 / 2.75 ? 7.5625 * (a -= 1.5 / 2.75) * a + .75 : a < 2.5 / 2.75 ? 7.5625 * (a -= 2.25 / 2.75) * a + .9375 : 7.5625 * (a -= 2.625 / 2.75) * a + .984375
        }, $InOutBounce: function (a) {
            return a < 1 / 2 ? g.$InBounce(a * 2) * .5 : g.$OutBounce(a * 2 - 1) * .5 + .5
        }, $GoBack: function (a) {
            return 1 - c.P(2 - 1)
        }, $InWave: function (a) {
            return 1 - c.Cb(a * c.u * 2)
        }, $OutWave: function (a) {
            return c.gb(a * c.u * 2)
        }, $OutJump: function (a) {
            return 1 - ((a *= 2) < 1 ? (a = 1 - a) * a * a : (a -= 1) * a * a)
        }, $InJump: function (a) {
            return (a *= 2) < 1 ? a * a * a : (a = 2 - a) * a * a
        }, $Early: c.H, $Late: c.G, $Mid: c.$Round, $Mid2: r(2), $Mid3: r(3), $Mid4: r(4), $Mid5: r(5), $Mid6: r(6)
    };

    function v(k, l, p) {
        var d = this, f = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, k || 0, l || 0, p || 0, 1], j = c.gb, i = c.Cb, n = c.Oe;

        function h(a) {
            return a * c.u / 180
        }

        function o(b, c, f, g, i, l, n, o, q, t, u, w, y, A, C, F, a, d, e, h, j, k, m, p, r, s, v, x, z, B, D, E) {
            return [b * a + c * j + f * r + g * z, b * d + c * k + f * s + g * B, b * e + c * m + f * v + g * D, b * h + c * p + f * x + g * E, i * a + l * j + n * r + o * z, i * d + l * k + n * s + o * B, i * e + l * m + n * v + o * D, i * h + l * p + n * x + o * E, q * a + t * j + u * r + w * z, q * d + t * k + u * s + w * B, q * e + t * m + u * v + w * D, q * h + t * p + u * x + w * E, y * a + A * j + C * r + F * z, y * d + A * k + C * s + F * B, y * e + A * m + C * v + F * D, y * h + A * p + C * x + F * E]
        }

        function g(b, a) {
            return o.apply(e, (a || f).concat(b))
        }

        d.$Scale = function (a, b, c) {
            if (a != 1 || b != 1 || c != 1) f = g([a, 0, 0, 0, 0, b, 0, 0, 0, 0, c, 0, 0, 0, 0, 1])
        };
        d.$Move = function (a, b, c) {
            f[12] += a || 0;
            f[13] += b || 0;
            f[14] += c || 0
        };
        d.$RotateX = function (b) {
            if (b) {
                a = h(b);
                var c = i(a), d = j(a);
                f = g([1, 0, 0, 0, 0, c, d, 0, 0, -d, c, 0, 0, 0, 0, 1])
            }
        };
        d.$RotateY = function (b) {
            if (b) {
                a = h(b);
                var c = i(a), d = j(a);
                f = g([c, 0, -d, 0, 0, 1, 0, 0, d, 0, c, 0, 0, 0, 0, 1])
            }
        };
        d.Cg = function (a) {
            d.Vg(h(a))
        };
        d.Vg = function (a) {
            if (a) {
                var b = i(a), c = j(a);
                f = g([b, c, 0, 0, -c, b, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
            }
        };
        d.Ug = function (a, b) {
            if (a || b) {
                k = h(a);
                l = h(b);
                f = g([1, n(l), 0, 0, n(k), 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
            }
        };
        d.Sg = function () {
            return "matrix3d(" + f.join(",") + ")"
        };
        d.Og = function () {
            return "matrix(" + [f[0], f[1], f[4], f[5], f[12], f[13]].join(",") + ")"
        }
    }

    var b = i.$Jssor$ = new function () {
        var a = this, Eb = /\S+/g, R = 1, mb = 2, qb = 3, pb = 4, tb = 5, T, t = 0, n = 0, I = 0, M = navigator,
            Ab = M.appName, o = M.userAgent, r = parseFloat;

        function w(c, a, b) {
            return c.indexOf(a, b)
        }

        function Qb() {
            if (!T) {
                T = {td: "ontouchstart" in i || "createTouch" in h};
                var a;
                if (M.pointerEnabled || (a = M.msPointerEnabled)) T.re = a ? "msTouchAction" : "touchAction"
            }
            return T
        }

        function y(g) {
            if (!t) {
                t = -1;
                if (Ab == "Microsoft Internet Explorer" && !!i.attachEvent && !!i.ActiveXObject) {
                    var e = w(o, "MSIE");
                    t = R;
                    n = r(o.substring(e + 5, w(o, ";", e)))
                } else if (Ab == "Netscape" && !!i.addEventListener) {
                    var d = w(o, "Firefox"), b = w(o, "Safari"), f = w(o, "Chrome"), c = w(o, "AppleWebKit");
                    if (d >= 0) {
                        t = mb;
                        n = r(o.substring(d + 8))
                    } else if (b >= 0) {
                        var h = o.substring(0, b).lastIndexOf("/");
                        t = f >= 0 ? pb : qb;
                        n = r(o.substring(h + 1, b))
                    } else {
                        var a = /Trident\/.*rv:([0-9]{1,}[\.0-9]{0,})/i.exec(o);
                        if (a) {
                            t = R;
                            n = r(a[1])
                        }
                    }
                    if (c >= 0) I = r(o.substring(c + 12))
                } else {
                    var a = /(opera)(?:.*version|)[ \/]([\w.]+)/i.exec(o);
                    if (a) {
                        t = tb;
                        n = r(a[2])
                    }
                }
            }
            return g == t
        }

        function F() {
            return y(R)
        }

        function ob() {
            return y(qb)
        }

        function sb() {
            return y(tb)
        }

        function B() {
            y();
            return I > 537 || n > 42 || t == R && n >= 11
        }

        function U(a) {
            var b;
            return function (d) {
                if (!b) {
                    var c = a.substr(0, 1).toUpperCase() + a.substr(1);
                    b = j(["", "WebKit", "ms", "Moz", "O", "webkit"], function (b) {
                        var e = b + (b ? c : a);
                        return d.style[e] != f && e
                    }) || a
                }
                return b
            }
        }

        var O = l("transform", 8);

        function J(a) {
            return a
        }

        function P(a) {
            return i.SVGElement && a instanceof i.SVGElement
        }

        function Ob(a) {
            return {}.toString.call(a)
        }

        var S = Array.isArray || function (a) {
            return N(a) == "array"
        }, wb = {};
        j(["Boolean", "Number", "String", "Function", "Array", "Date", "RegExp", "Object"], function (a) {
            wb["[object " + a + "]"] = a.toLowerCase()
        });

        function j(b, d) {
            var a, c;
            if (S(b)) {
                for (a = 0; a < m(b); a++) if (c = d(b[a], a, b)) return c
            } else for (a in b) if (c = d(b[a], a, b)) return c
        }

        function N(a) {
            return a == e ? String(a) : wb[Ob(a)] || "object"
        }

        function Z(a) {
            for (var b in a) return d
        }

        function D(a) {
            try {
                return N(a) == "object" && !a.nodeType && a != a.window && (!a.constructor || {}.hasOwnProperty.call(a.constructor.prototype, "isPrototypeOf"))
            } catch (b) {
            }
        }

        function Db(a, b) {
            return {x: a, y: b}
        }

        function Rb(b, a) {
            setTimeout(b, a || 0)
        }

        function q(a, b) {
            return a === f ? b : a
        }

        a.ud = Qb;
        a.ue = F;
        a.He = ob;
        a.gg = B;
        a.Cd = function () {
            return n
        };
        a.$Delay = Rb;
        a.wc = q;
        a.W = function (a, b) {
            b.call(a);
            return x({}, a)
        };

        function bb(a) {
            a.constructor === bb.caller && a.F && a.F.apply(a, bb.caller.arguments)
        }

        a.F = bb;
        a.$GetElement = function (b) {
            if (a.ag(b)) b = h.getElementById(b);
            return b
        };
        a.xc = function (c) {
            var b = [];
            j(c, function (d) {
                var c = a.$GetElement(d);
                c && b.push(c)
            });
            return b
        };

        function u(a) {
            return a || i.event
        }

        a.Zf = u;
        a.$EvtSrc = function (c) {
            c = u(c);
            var b = c.target || c.srcElement || h;
            if (b.nodeType == 3) b = a.Lb(b);
            return b
        };
        a.Fe = function (a) {
            a = u(a);
            return a.relatedTarget || a.toElement
        };
        a.Je = function (a) {
            a = u(a);
            return a.which || ([0, 1, 3, 0, 2])[a.button] || a.charCode || a.keyCode
        };
        a.Tc = function (a) {
            a = u(a);
            return {x: a.clientX || 0, y: a.clientY || 0}
        };
        a.Ue = function (a, b) {
            return Db(a.x - b.x, a.y - b.y)
        };
        a.eg = function (a, b) {
            return a.x >= b.x && a.x <= b.t && a.y >= b.y && a.y <= b.m
        };
        a.Ie = function (d, f) {
            var c = b.dg(f), e = b.Tc(d);
            return a.eg(e, c)
        };
        a.Ib = function (b) {
            return P(a.Lb(b))
        };

        function A(c, d, a) {
            if (a !== f) c.style[d] = a == f ? "" : a; else {
                var b = c.currentStyle || c.style;
                a = b[d];
                if (a == "" && i.getComputedStyle) {
                    b = c.ownerDocument.defaultView.getComputedStyle(c, e);
                    b && (a = b.getPropertyValue(d) || b[d])
                }
                return a
            }
        }

        function fb(b, c, a, d) {
            if (a === f) {
                a = r(A(b, c));
                isNaN(a) && (a = e);
                return a
            }
            d && a != e && (a += d);
            A(b, c, a)
        }

        function l(g, a, b, d) {
            var c;
            if (a & 2) c = "px";
            if (a & 4) c = "%";
            if (a & 16) c = "em";
            var f = a & 8 && U(g);
            a &= -9;
            d = d || (a ? fb : A);
            return function (i, h) {
                b && h && (h *= b);
                var a = d(i, f ? f(i) : g, h, c);
                return b && a != e ? a / b : a
            }
        }

        function C(a) {
            return function (c, b) {
                s(c, a, b)
            }
        }

        var hb = {
            r: ["rotate"],
            sX: ["scaleX", 2],
            sY: ["scaleY", 2],
            tX: ["translateX", 1],
            tY: ["translateY", 1],
            kX: ["skewX"],
            kY: ["skewY"]
        };

        function jb(a) {
            var b = "";
            if (a) {
                j(a, function (d, c) {
                    var a = hb[c];
                    if (a) {
                        var e = a[1] || 0;
                        if (ib[c] != d) b += " " + a[0] + "(" + d + (["deg", "px", ""])[e] + ")"
                    }
                });
                if (B()) if (a.tX || a.tY || a.tZ != f) b += " translate3d(" + (a.tX || 0) + "px," + (a.tY || 0) + "px," + (a.tZ || 0) + "px)"
            }
            return b
        }

        function nb(a) {
            return "rect(" + a.y + "px " + a.t + "px " + a.m + "px " + a.x + "px)"
        }

        a.ug = l("transformOrigin", 8);
        a.tg = l("backfaceVisibility", 8);
        a.Jc = l("transformStyle", 8);
        a.yg = l("perspective", 10);
        a.xg = l("perspectiveOrigin", 8);
        a.we = function (b, a) {
            O(b, a == 1 ? "" : "scale(" + a + ")")
        };
        a.$AddEvent = function (b, c, d, e) {
            b = a.$GetElement(b);
            b.addEventListener(c, d, e)
        };
        a.$RemoveEvent = function (b, c, d, e) {
            b = a.$GetElement(b);
            b.removeEventListener(c, d, e)
        };
        a.$CancelEvent = function (a) {
            a = u(a);
            a.preventDefault && a.preventDefault();
            a.cancel = d;
            a.returnValue = k
        };
        a.$StopEvent = function (a) {
            a = u(a);
            a.stopPropagation && a.stopPropagation();
            a.cancelBubble = d
        };
        a.Z = function (d, c) {
            var a = [].slice.call(arguments, 2), b = function () {
                var b = a.concat([].slice.call(arguments, 0));
                return c.apply(d, b)
            };
            return b
        };
        a.bd = function (b, c) {
            if (c == f) return b.textContent || b.innerText;
            var d = h.createTextNode(c);
            a.Rb(b);
            b.appendChild(d)
        };
        a.ng = function (a, b) {
            if (b == f) return a.innerHTML;
            a.innerHTML = b
        };
        a.dg = function (b) {
            var a = b.getBoundingClientRect();
            return {x: a.left, y: a.top, w: a.right - a.left, h: a.bottom - a.top, t: a.right, m: a.bottom}
        };
        a.jb = function (d, c) {
            for (var b = [], a = d.firstChild; a; a = a.nextSibling) (c || a.nodeType == 1) && b.push(a);
            return b
        };

        function zb(a, c, f, b) {
            b = b || "u";
            for (a = a ? a.firstChild : e; a; a = a.nextSibling) if (a.nodeType == 1) {
                if (K(a, b) == c) return a;
                if (!f) {
                    var d = zb(a, c, f, b);
                    if (d) return d
                }
            }
        }

        a.$FindChild = zb;

        function Y(a, d, g, b) {
            b = b || "u";
            var c = [];
            for (a = a ? a.firstChild : e; a; a = a.nextSibling) if (a.nodeType == 1) {
                K(a, b) == d && c.push(a);
                if (!g) {
                    var f = Y(a, d, g, b);
                    if (m(f)) c = c.concat(f)
                }
            }
            return c
        }

        a.rg = function (b, a) {
            return b.getElementsByTagName(a)
        };
        a.kb = function (a, f, d, g) {
            d = d || "u";
            var e;
            do {
                if (a.nodeType == 1) {
                    var c;
                    d && (c = K(a, d));
                    if (c && c == q(f, c) || g == a.tagName) {
                        e = a;
                        break
                    }
                }
                a = b.Lb(a)
            } while (a && a != h.body);
            return e
        };
        a.qe = function (a) {
            return db(["INPUT", "TEXTAREA", "SELECT"])[a.tagName]
        };

        function x() {
            for (var d = arguments, h = 1 & d[0], e = 1 + h, g = d[e - 1] || {}, c, b, a; e < m(d); e++) if (c = d[e]) for (b in c) {
                a = c[b];
                if (a !== f) {
                    a = c[b];
                    var i = g[b];
                    g[b] = h && (D(i) || D(a)) ? x(h, {}, i, a) : a
                }
            }
            return g
        }

        a.v = x;

        function cb(f, g) {
            var d = {}, c, a, b;
            for (c in f) {
                a = f[c];
                b = g[c];
                if (a !== b) {
                    var e = k;
                    if (D(a) && D(b)) {
                        a = cb(a, b);
                        e = !Z(a)
                    }
                    !e && (d[c] = a)
                }
            }
            return d
        }

        a.Zg = cb;
        a.Pd = function (a, c) {
            if (a) {
                var b;
                j(c, function (c) {
                    if (a[c] != f) (b = b || {})[c] = a[c];
                    delete a[c]
                });
                return b
            }
        };
        a.Ph = function (a) {
            return N(a) == "function"
        };
        a.Md = S;
        a.ag = function (a) {
            return N(a) == "string"
        };
        a.Nd = function (a) {
            return !S(a) && !isNaN(r(a)) && isFinite(a)
        };
        a.f = j;
        a.Th = Z;
        a.Sh = D;

        function W(a) {
            return h.createElement(a)
        }

        a.bc = function () {
            return W("DIV")
        };
        a.Rd = function () {
            return W("SPAN")
        };
        a.Kc = function () {
        };

        function s(b, c, a, d) {
            if (a === f) return b.getAttribute(c);
            a = a == e ? "" : d ? a + d : a;
            b.setAttribute(c, a)
        }

        function K(a, b) {
            return s(a, b) || s(a, "data-" + b)
        }

        a.g = s;
        a.hb = K;
        a.q = function (e, c, d) {
            var b = a.od(K(e, c));
            if (isNaN(b)) b = d;
            return b
        };
        a.Hc = function (b, c, a) {
            return eb(s(b, c), a)
        };

        function G(b, a) {
            return s(b, "class", a) || ""
        }

        function db(b) {
            var a = {};
            j(b, function (b) {
                if (b != f) a[b] = b
            });
            return a
        }

        function eb(a, b) {
            return a && a.match(b || Eb) || e
        }

        function V(b, a) {
            return db(eb(b || "", a))
        }

        a.Fd = db;
        a.Ud = eb;
        a.mg = function (a) {
            a && (a = a.toLowerCase());
            return a
        };

        function gb(b, c) {
            var a = "";
            j(c, function (c) {
                a && (a += b);
                a += c
            });
            return a
        }

        function Q(a, c, b) {
            G(a, gb(" ", x(cb(V(G(a)), V(c)), V(b))))
        }

        a.je = gb;
        a.Lb = function (a) {
            return a.parentNode
        };
        a.Fc = function (b) {
            a.nb(b, "none")
        };
        a.mb = function (b, c) {
            a.nb(b, q(c, d) ? "" : "none")
        };
        a.Oh = function (b, a) {
            b.removeAttribute(a)
        };
        a.kh = function (b, a) {
            b.style.clip = nb(a)
        };
        a.Tb = function () {
            return +new Date
        };
        a.O = function (b, a) {
            b.appendChild(a)
        };
        a.ph = function (c, b) {
            j(b, function (b) {
                a.O(c, b)
            })
        };
        a.pb = function (b, a, c) {
            (c || a.parentNode).insertBefore(b, a)
        };
        a.oh = function (b, a, c) {
            b.insertAdjacentHTML(a, c)
        };
        a.ib = function (b, a) {
            a = a || b.parentNode;
            a && a.removeChild(b)
        };
        a.ch = function (b, c) {
            j(b, function (b) {
                a.ib(b, c)
            })
        };
        a.Rb = function (b) {
            a.ch(a.jb(b, d), b)
        };

        function Bb() {
            j([].slice.call(arguments, 0), function (b) {
                if (a.Md(b)) Bb.apply(e, b); else b && b.$Destroy && b.$Destroy()
            })
        }

        a.$Destroy = Bb;
        a.Uc = function (b, c) {
            var d = a.Lb(b);
            if (c & 1) {
                a.U(b, (a.K(d) - a.K(b)) / 2);
                a.Vd(b, e)
            }
            if (c & 2) {
                a.V(b, (a.J(d) - a.J(b)) / 2);
                a.be(b, e)
            }
        };
        var X = {$Top: e, $Right: e, $Bottom: e, $Left: e, Eb: e, Gb: e};
        a.Ch = function (b) {
            var c = a.bc();
            L(c, {Me: "block", Pb: a.db(b), $Top: 0, $Left: 0, Eb: 0, Gb: 0});
            var e = a.ve(b, X);
            a.pb(c, b);
            a.O(c, b);
            var f = a.ve(b, X), d = {};
            j(e, function (b, a) {
                if (b == f[a]) d[a] = b
            });
            L(c, X);
            L(c, d);
            L(b, {$Top: 0, $Left: 0});
            return d
        };
        a.Fh = function (b, a) {
            return parseInt(b, a || 10)
        };
        a.od = r;
        a.Ae = function (b, a) {
            var c = h.body;
            while (a && b !== a && c !== a) a = a.parentNode;
            return b === a
        };

        function ab(e, d, c) {
            var b = e.cloneNode(!d);
            !c && a.Oh(b, "id");
            return b
        }

        a.ab = ab;
        a.Vb = function (f, g) {
            var b = new Image;

            function c(f, d) {
                a.$RemoveEvent(b, "load", c);
                a.$RemoveEvent(b, "abort", e);
                a.$RemoveEvent(b, "error", e);
                g && g(b, d)
            }

            function e(a) {
                c(a, d)
            }

            if (sb() && n < 11.6 || !f) c(!f); else {
                a.$AddEvent(b, "load", c);
                a.$AddEvent(b, "abort", e);
                a.$AddEvent(b, "error", e);
                b.src = f
            }
        };
        a.Eh = function (g, c, f) {
            var d = 1;

            function e(a) {
                d--;
                if (c && a && a.src == c.src) c = a;
                !d && f && f(c)
            }

            j(g, function (f) {
                var c = b.hb(f, "src");
                if (c) {
                    d++;
                    a.Vb(c, e)
                }
            });
            e()
        };
        a.Ce = function (a, g, i, h) {
            if (h) a = ab(a);
            var c = Y(a, g);
            if (!m(c)) c = b.rg(a, g);
            for (var f = m(c) - 1; f > -1; f--) {
                var d = c[f], e = ab(i);
                G(e, G(d));
                b.th(e, d.style.cssText);
                b.pb(e, d);
                b.ib(d)
            }
            return a
        };

        function Lb() {
            var c = this;
            b.W(c, p);
            var e, q = "", t = ["av", "pv", "ds", "dn"], g = [], r, n = 0, l = 0, k = 0;

            function m() {
                Q(e, r, (g[k || l & 2 || l] || "") + " " + (g[n] || ""));
                a.lc(e, k ? "none" : "")
            }

            function d() {
                n = 0;
                c.T(i, "mouseup", d);
                c.T(h, "mouseup", d);
                c.T(h, "touchend", d);
                c.T(h, "touchcancel", d);
                c.T(i, "blur", d);
                m()
            }

            function o() {
                n = 4;
                m();
                c.a(i, "mouseup", d);
                c.a(h, "mouseup", d);
                c.a(h, "touchend", d);
                c.a(h, "touchcancel", d);
                c.a(i, "blur", d)
            }

            c.Ye = function (a) {
                if (a === f) return l;
                l = a & 2 || a & 1;
                m()
            };
            c.$Enable = function (a) {
                if (a === f) return !k;
                k = a ? 0 : 3;
                m()
            };
            c.F = function (f) {
                c.$Elmt = e = a.$GetElement(f);
                s(e, "data-jssor-button", "1");
                var d = b.Ud(G(e));
                if (d) q = d.shift();
                j(t, function (a) {
                    g.push(q + a)
                });
                r = gb(" ", g);
                g.unshift("");
                c.a(e, "mousedown", o);
                c.a(e, "touchstart", o)
            };
            b.F(c)
        }

        a.Lc = function (a) {
            return new Lb(a)
        };
        a.xh = function (a, b) {
            return c.xb(a * a + b * b)
        };
        a.R = A;
        l("backgroundColor");
        a.Fb = l("overflow");
        a.lc = l("pointerEvents");
        a.V = l("top", 2);
        a.U = l("left", 2);
        a.cb = l("opacity", 1);
        a.N = l("zIndex", 1);

        function yb(m, n, a, k, b, g, f) {
            if (b) {
                var h = b[0], d = b[1];
                if (f) {
                    var e = c.l(d * 2, 1), l = e * (f - 1) + 1;
                    a = (a * l - h) / e;
                    if (a > 0) {
                        d /= e;
                        h = 0;
                        var j = c.H(a) - 1;
                        a = a - j;
                        if (a > d && j < f - 1) a = 1 - a
                    }
                }
                a = (a - h) / d;
                a = c.j(c.l(a, 0), 1)
            }
            if (g) {
                a = a * g;
                var i = c.G(a);
                a - i && (a -= i);
                a = c.j(c.l(a, 0), 1)
            }
            if (b || g) a = c.Y(a, 3);
            return m + n * k(a)
        }

        function kb(d, e, h, i) {
            d = d || {};
            var g = {}, b = {};

            function n(a) {
                b[a] = d[a]
            }

            function l() {
                b.cc = d.x;
                h && !e && (b.cc -= h)
            }

            function m() {
                b.Wb = d.y;
                i && !e && (b.Wb -= i)
            }

            var k = {cc: 0, Wb: 0, sX: 1, sY: 1, r: 0, rX: 0, rY: 0, tX: 0, tY: 0, tZ: 0, kX: 0, kY: 0}, c = {};
            if (!B() || e) {
                c.tZ = a.Kc;
                c.tX = a.Kc;
                c.tY = a.Kc
            }
            if (B() || e) {
                c.x = l;
                c.y = m
            }
            j(d, function (b, a) {
                (c[a] || n)(a)
            });
            j(b, function (c, a) {
                if (k[a] != f) {
                    g[a] = c;
                    delete b[a]
                }
            });
            Z(g) && (b.Kd = g);
            return b
        }

        function vb(f, e) {
            var b = [], h = e & 1;
            e & 2 && (h = !h);
            for (var k = c.H(f / 2), a = 0; a < f; a++) {
                var d = a;
                if (e & 4) {
                    var g = c.G(c.dd() * f);
                    d = q(b[a], a);
                    b[a] = q(b[g], g);
                    b[g] = d
                } else {
                    if (e & 2) {
                        d = a < k ? a * 2 : (f - a - 1) * 2 + 1;
                        b[d] = a
                    }
                    if (e & 32) d = c.G(a / 2) + (a % 2 ? c.H(k) : 0);
                    b[d] = a
                }
            }
            h && b.reverse();
            var i = [];
            j(b, function (b, a) {
                i[b] = a
            });
            return i
        }

        function xb(b, h, e, d) {
            for (var g = [], i = e ? c.H((b + d) / 2) : b, f = 1 / (h * (i - 1) + 1), a = 0; a < b; a++) {
                var j = e ? c.G((a + d) / 2) : a;
                g[a] = [j * h * f, f]
            }
            return g
        }

        function Jb(h, u, e) {
            h = h || {d: e.$Elmt ? s(e.$Elmt, "d") : ""};
            var E = e.$Easing, k = e.Bd || {}, g = k.r, z = g == 0, F = k.dl || 0;

            function x(c, a) {
                var d = c[0], o = c[1], e = c[2], p = c[3], g = c[4], q = c[5], h = c[6], r = c[7];
                if (a === f) a = .5;
                var b = 1 - a, i = b * d + a * e, s = b * o + a * p, j = b * e + a * g, t = b * p + a * q,
                    k = b * g + a * h, u = b * q + a * r, l = b * i + a * j, v = b * s + a * t, m = b * j + a * k,
                    w = b * t + a * u, n = b * l + a * m, x = b * v + a * w;
                return [[d, o, i, s, l, v, n, x], [n, x, m, w, k, u, h, r]]
            }

            function w(c, g) {
                for (var d = 0, e = 0, a = 0, b = g ? 6 : 0; b < m(c); b += 6) {
                    d += c[b];
                    e += c[b + 1];
                    a++
                }
                return {x: a ? d / a : f, y: a ? e / a : f}
            }

            function b(b) {
                var l = m(b), j = b[0] == b[l - 2] && b[1] == b[l - 1], g = w(b, j), k = [], h = [];

                function e(a) {
                    return {x: b[a], y: b[a + 1]}
                }

                function f(j, f, b) {
                    var d = a.Ue(j, f);
                    h[b] = a.xh(d.x, d.y);
                    if (!h[b] && b % 6) {
                        var g = b % 6 < 3 ? 2 : -2;
                        d = a.Ue(e(b + g), f)
                    }
                    var i = c.Yf(d.y, d.x);
                    k[b] = i
                }

                for (var d = 0; d < m(b); d += 6) {
                    var i = e(d);
                    f(i, g, d);
                    f(e(d - 2), i, d - 2);
                    f(e(d + 2), i, d + 2)
                }
                return {lb: b, qb: (m(b) - 2) / 6, kc: g.x, ic: g.y, Nc: k, Vc: h, vc: j}
            }

            function n(o) {
                function i(a) {
                    return a.replace(/[\^\s]*([mhvlzcsqta]|\-?\d*\.?\d+)[,\$\s]*/gi, " $1").replace(/([mhvlzcsqta])/gi, " $1").trim().split("  ").map(l)
                }

                function l(a) {
                    return a.split(" ").map(k)
                }

                function k(a, b) {
                    return b === 0 ? a : +a
                }

                var h = [], a, n = i(o || ""), d, e, f, g;

                function c(b) {
                    f = b[m(b) - 2];
                    g = b[m(b) - 1];
                    a = a.concat(b)
                }

                j(n, function (i) {
                    var j = i.shift();
                    switch (j) {
                        case"M":
                            a && h.push(b(a));
                            a = [];
                            d = i[0];
                            e = i[1];
                            c(i);
                            break;
                        case"L":
                            c([f, g, i[0], i[1], i[0], i[1]]);
                            break;
                        case"C":
                            c(i);
                            break;
                        case"Z":
                        case"z":
                            (f != d || g != e) && c([f, g, d, e, d, e])
                    }
                });
                a && h.push(b(a));
                return h
            }

            function d(a, b) {
                return c.Y(a, 2) + "," + c.Y(b, 2)
            }

            function A(a) {
                for (var c = "M" + d(a[0], a[1]), b = 2; b < m(a) - 2; b += 6) {
                    c += "C";
                    c += d(a[b], a[b + 1]) + " ";
                    c += d(a[b + 2], a[b + 3]) + " ";
                    c += d(a[b + 4], a[b + 5])
                }
                return c
            }

            function y(b) {
                var a = "";
                j(b, function (b) {
                    a += A(b)
                });
                return a
            }

            function D(d) {
                for (var c = [], a = 0; a < m(d) - 2; a += 6) c.push(b(d.slice(a, a + 8)));
                return c
            }

            function B(c) {
                var a = [];
                j(c, function (c, d) {
                    var b = c.lb;
                    !d && a.push(b[0], b[1]);
                    a = a.concat(b.slice(2))
                });
                return b(a)
            }

            function l(d, a) {
                var p = a.gf = [], q = a.bf = [], e = a.qb + (!d.vc || !d.vc);

                function n(b) {
                    return a.Nc[b] - d.Nc[b]
                }

                function h(b, a) {
                    a = a || 0;
                    return c.Y((b - a + c.u * 101) % (c.u * 2) - c.u + a, 8)
                }

                function i(b, f) {
                    var e = d.Vc[b], g = a.Vc[b], i = g - e, c = n(b);
                    c = h(c, f);
                    p[b] = i;
                    q[b] = c;
                    return c
                }

                for (var l = 0, b = 0; b < e; b++) l += h(n(b * 6));
                var f = h(l / e);
                if (g) {
                    var j = g > 0 ? 1 : -1;
                    f = (f + c.u * 2 * j) % (c.u * 2) || c.u * 2 * j;
                    f += c.u * 2 * (g - j)
                }
                for (var b = 0; b < m(d.lb); b += 6) {
                    var o = i(b, f);
                    i(b - 2, o);
                    i(b + 2, o)
                }
                var s = xb(e, F), r = vb(e, k.o);
                a.ad = function (b, c) {
                    if (b >= 0 && b <= a.qb) return yb(0, 1, c, E, s[r[b % e]])
                }
            }

            function t(d, a, s, n, i) {
                function q(d) {
                    for (var a = [0, .2, 0, .09, .09, 0, .2, 0, .31, 0, .4, .09, .4, .2, .4, .31, .31, .4, .2, .4, .09, .4, 0, .31, 0, .2], c = 0; c < m(a); c += 2) {
                        a[c] += d.kc - .2;
                        a[c + 1] += d.ic - .2
                    }
                    var e = b(a);
                    e.vc = d.vc;
                    return e
                }

                d = s[i] = d || q(a);
                a = n[i] = a || q(d);
                var h = d.qb, g = a && a.qb;
                if (h < g) return t(a, d, n, s, i);
                if (g < h) {
                    for (var r = D(a.lb), u = h / g, o = h - g, f = 0, p = 0; p < 10 && f < o; p++) {
                        var v = u + u * p / 10, e = 0;
                        j(r, function (d, g) {
                            e += d.qb;
                            var b = c.$Round((g + 1) * v);
                            if (e < b) {
                                var a = c.j(b - e, o - f);
                                d.qb += a;
                                f += a;
                                e += a
                            }
                            return o < f
                        })
                    }
                    var k = [];
                    j(r, function (d) {
                        var a = d.qb, c = d.lb;
                        while (a - 1) {
                            var e = x(c, 1 / a);
                            k.push(b(e[0]));
                            c = e[1];
                            a--
                        }
                        k.push(b(c))
                    });
                    a = n[i] = B(k)
                }
                l(d, a);
                l(a, d)
            }

            function r(b, a) {
                if (m(b) < m(a)) return r(a, b);
                j(b, function (d, c) {
                    t(d, a[c], b, a, c)
                })
            }

            var o = n(h.d), p = n(u.d);
            r(o, p);

            function i(b, h, i, e, a, l) {
                var d = b.lb;
                if (a >= 0 && a < m(b.lb)) {
                    var k = h.lb, f, g;
                    if (z) {
                        f = d[a] + (k[a] - d[a]) * e;
                        g = d[a + 1] + (k[a + 1] - d[a + 1]) * e
                    } else {
                        var o = b.Vc[a], p = h.gf[a], q = b.Nc[a], r = h.bf[a], j = o + p * e, n = q + r * e;
                        f = j * c.Cb(n) + i.x;
                        g = j * c.gb(n) + i.y
                    }
                    l[a] = f;
                    l[a + 1] = g;
                    return {x: f, y: g}
                }
            }

            var v = {
                E: function (a) {
                    if (!a) return h;
                    if (a == 1) return u;
                    var b = [];
                    j(o, function (c, n) {
                        for (var g = [], d = p[n], e = 0; e < m(c.lb); e += 6) {
                            var f = d.ad(e / 6, a), l = q(d.ad(e / 6 - 1, a), f), k = q(d.ad(e / 6 + 1, a), f),
                                j = {x: c.kc + (d.kc - c.kc) * f, y: c.ic + (d.ic - c.ic) * f}, h = i(c, d, j, f, e, g);
                            i(c, d, h, (f + l) / 2, e - 2, g);
                            i(c, d, h, (f + k) / 2, e + 2, g)
                        }
                        b.push(g)
                    });
                    return {d: y(b)}
                }, X: function (a) {
                    return a && a.d || ""
                }, sb: C("d")
            };
            return v
        }

        function Hb(b) {
            return x({wc: a.Ph(b) ? b : g.$Linear}, b)
        }

        function z(i, u, h, M, o) {
            i = i || {};
            h = x({}, h);
            var ab = h.$Elmt, p = {}, W = {}, w, y, r = h.le, P = h.Ib, F = k(Hb(h.$Easing)), V = k(h.Bd),
                X = k(h.$During), Z = k(h.$Round), Y = k(h.Pc, E), G = S(u);
            i = k(i, f, d);
            u = k(u, f, d);
            var U = B(), K = o ? {
                c: R,
                Kd: L,
                pt: Jb,
                bl: Q,
                da: H,
                fc: n(C("fill"), [0, 0, 0, 1]),
                sc: n(C("stroke")),
                cl: n(l("color"), [0, 0, 0, 1]),
                bgc: n(l("backgroundColor")),
                bdc: n(l("borderColor")),
                rp: N
            } : {}, s = h.Yc || o && {o: 4, so: 4, Kd: 4, ls: 4, lh: 4, sX: 4, sY: 4};

            function T(c) {
                var d = V[c] || {};
                return b.v({}, h, {
                    $Easing: F[c] || F.wc || e,
                    Pc: Y[c] || e,
                    Bd: d,
                    $During: X[c] || e,
                    $Round: Z[c] || e,
                    Mf: d.rd,
                    Yc: a.Nd(s) ? s : s && s[c],
                    le: 0
                })
            }

            function t(a) {
                return m(a) % 2 ? a.concat(a) : a
            }

            function k(a, c, b) {
                a = M ? kb(a, P, b && h.Lf, b && h.Of) : a || {};
                return o ? x({}, c, a) : a
            }

            function n(f, d) {
                function c(a) {
                    return a == "transparent" ? e : a || d
                }

                function a(a, b) {
                    a = c(a);
                    b = c(b);
                    if (!a && b) {
                        a = b.slice(0);
                        a[3] = 0
                    }
                    return a || [0, 0, 0, 0]
                }

                return function (c, d, g) {
                    d = a(d, c);
                    c = a(c, d);
                    var e = z(c, d, b.v({Yc: [0, 0, 0, 4]}, g));
                    return {
                        E: function (a) {
                            return e.E(a)
                        }, X: function (a) {
                            return "rgba(" + a.join(",") + ")"
                        }, sb: f
                    }
                }
            }

            function I(b, k, a) {
                b = b || 0;
                var f = a.$Easing || g.$Linear, e = a.$During, i = a.$Round, h = a.Mf, j = k - b, d = q(a.Yc, 2);
                return {
                    E: function (a) {
                        return c.Y(yb(b, j, a, f, e, i, h), d)
                    }, X: J, sb: a.Pc
                }
            }

            function A(c, d, a, b) {
                return {
                    E: z(c, d, a).E, X: function (a) {
                        return a.join(",")
                    }, sb: b
                }
            }

            function Q(b, c, a) {
                return A(t(b || [0]), t(c), a, C("stdDeviation"))
            }

            function H(a, c, h) {
                var e = m(c);
                c = t(c);
                if (!a) {
                    a = c.slice(0);
                    j(a, function (c, b) {
                        b % 2 && (a[b] = 0)
                    })
                }
                a = t(a);
                for (var d = m(a), f, b = 1; b <= d && b <= e; b++) if (!(d % b) && !(e % b)) f = b;

                function g(b) {
                    var a = b;
                    while (m(a) < d * e / f) a = a.concat(b);
                    return a
                }

                return A(g(a), g(c), h, C("stroke-dasharray"))
            }

            function R(b, c, a) {
                return {
                    E: z(b, c, a).E, X: function (b) {
                        return (b.y || b.x || b.m - a.$OriginalHeight || b.t - a.$OriginalWidth) && nb(b) || ""
                    }, sb: l("clip")
                }
            }

            function L(e, f, c) {
                var a = c.Nf, b;

                function d(b) {
                    var d = (b.rX || 0) % 360, e = (b.rY || 0) % 360, f = (b.r || 0) % 360, g = q(b.sX, 1),
                        h = q(b.sY, 1), i = q(b.sZ, 1), c = new v(b.tX, b.tY, b.tZ || 0);
                    a && c.$Move(-a.x, -a.y);
                    c.$Scale(g, h, i);
                    c.Ug(b.kX, b.kY);
                    c.$RotateX(d);
                    c.$RotateY(e);
                    c.Cg(f);
                    a && c.$Move(a.x, a.y);
                    c.$Move(b.cc, b.Wb);
                    return c
                }

                if (c.Ib) {
                    y = C("transform");
                    b = function (a) {
                        return d(a).Og()
                    }
                } else {
                    y = O;
                    if (U) b = function (a) {
                        return d(a).Sg()
                    }; else b = jb
                }
                return {E: z(e, f, c).E, sb: y, X: b || J}
            }

            function N() {
                var b = 1e-5;
                return {
                    E: J, X: J, sb: function (d) {
                        b *= -1;
                        a.cb(d, c.Y(a.cb(d), 4) + b)
                    }
                }
            }

            j(u, function (b, a) {
                var c = i && i[a] || 0;
                if (G || b !== c) {
                    var d = o && K[a] || (D(b) ? z : I);
                    p[a] = d(c, b, T(a))
                }
            });
            w = function (b) {
                var a;
                j(p, function (c, e) {
                    var d = c.E(b);
                    c.sb(c.$Elmt || ab, c.X(d));
                    e == "o" && (a = d)
                });
                return a
            };
            r && b.f(p, function (a, e) {
                for (var d = [], b = 0; b < r + 1; b++) d[b] = a.X(a.E(b / r));
                W[e] = d;
                a.E = function (a) {
                    return d[c.$Round(a * r)]
                };
                a.X = J
            });
            w.E = function (c) {
                var a = x(d, G ? [] : {}, i);
                b.f(p, function (b, d) {
                    a[d] = b.E(c)
                });
                return a
            };
            return w
        }

        a.Kf = z;
        a.Zd = vb;
        a.K = l("width", 2);
        a.J = l("height", 2);
        a.Vd = l("right", 2);
        a.be = l("bottom", 2);
        l("marginLeft", 2);
        l("marginTop", 2);
        a.db = l("position");
        a.nb = l("display");
        a.th = function (a, b) {
            if (b != f) a.style.cssText = b; else return a.style.cssText
        };
        a.Jf = function (b, a) {
            if (a === f) {
                a = A(b, "backgroundImage") || "";
                var c = /\burl\s*\(\s*["']?([^"'\r\n,]+)["']?\s*\)/gi.exec(a) || [];
                return c[1]
            }
            A(b, "backgroundImage", a ? "url('" + a + "')" : "")
        };
        var E;
        a.If = E = {
            $Opacity: a.cb,
            $Top: a.V,
            $Right: a.Vd,
            $Bottom: a.be,
            $Left: a.U,
            Eb: a.K,
            Gb: a.J,
            Pb: a.db,
            Me: a.nb,
            $ZIndex: a.N,
            o: a.cb,
            x: a.U,
            y: a.V,
            i: a.N,
            dO: l("stroke-dashoffset", 1),
            ls: l("letterSpacing", 16),
            lh: l("lineHeight", 1),
            so: l("startOffset", 4, 100, s)
        };
        a.ve = function (c, b) {
            var a = {};
            j(b, function (d, b) {
                if (E[b]) a[b] = E[b](c)
            });
            return a
        };

        function L(b, a) {
            j(a, function (c, a) {
                E[a] && E[a](b, c)
            })
        }

        a.rb = L;
        var ib = {cc: 0, Wb: 0, sX: 1, sY: 1, r: 0, rX: 0, rY: 0, tX: 0, tY: 0, tZ: 0, kX: 0, kY: 0},
            Pb = [g.$Linear, g.$Swing, g.$InQuad, g.$OutQuad, g.$InOutQuad, g.$InCubic, g.$OutCubic, g.$InOutCubic, g.$InQuart, g.$OutQuart, g.$InOutQuart, g.$InQuint, g.$OutQuint, g.$InOutQuint, g.$InSine, g.$OutSine, g.$InOutSine, g.$InExpo, g.$OutExpo, g.$InOutExpo, g.$InCirc, g.$OutCirc, g.$InOutCirc, g.$InElastic, g.$OutElastic, g.$InOutElastic, g.$InBack, g.$OutBack, g.$InOutBack, g.$InBounce, g.$OutBounce, g.$InOutBounce, g.$Early, g.$Late, g.$Mid, g.$Mid2, g.$Mid3, g.$Mid4, g.$Mid5, g.$Mid6];

        function ub(a) {
            var c;
            if (b.Nd(a)) c = Pb[a]; else if (b.Sh(a)) {
                c = {};
                j(a, function (a, b) {
                    c[b] = ub(a)
                })
            }
            return c || a
        }

        a.Ld = ub;

        function m(a) {
            return a.length
        }

        a.A = m;
        a.Qd = w;
        a.Vf = function (k, j, n, o) {
            b.cb(k, 1);
            var m = {o: {j: 0, l: 1}}, e = {x: 0, y: 0, o: 1, r: 0, rX: 0, rY: 0, sX: 1, sY: 1, tZ: 0, kX: 0, kY: 0};

            function h(e) {
                var a = [], c = b.jb(e, d);
                b.f(c, function (d) {
                    if (d.nodeType == 3) {
                        for (var f = b.bd(d), e = 0; e < b.A(f); e++) {
                            var g = f[e], c = b.Rd();
                            b.nb(c, "inline-block");
                            b.db(c, "relative");
                            g == " " ? b.ng(c, "&nbsp;") : b.bd(c, g);
                            b.pb(c, d);
                            a.push(c);
                            b.cb(c, j)
                        }
                        b.ib(d)
                    } else a = a.concat(h(d))
                });
                return a
            }

            function l(n) {
                var j = this, h = b.Zd(a, 4), e = b.Pd(n, ["b", "d", "e", "p", "dr"]) || {}, g = {};

                function i(d, g, f) {
                    var b = f ? a : g, e = 0;
                    if (d.Sd & 2) {
                        b = c.H(b / 2);
                        if (!d.$Reverse) {
                            e = (b + 1) % 2 * d.ed;
                            b += e
                        }
                    }
                    return b
                }

                function d(d) {
                    var g = d & 1, i = d & 2 || 1, e = 0;
                    if (d & 2) e = a % 2;
                    var f = d == 68 ? h : b.Zd(a, d);
                    return {
                        Sd: d, ed: e, $Reverse: g, Od: f, Le: function (a) {
                            return c.G((f[a] + e * !g) / i)
                        }
                    }
                }

                function l(a, b, f, d) {
                    var e = i(a, b, f), c = 1 / (d * (e - 1) + 1);
                    return {
                        nc: function (e) {
                            return a.Od[e] < b && [a.Le(e) * d * c, c]
                        }
                    }
                }

                function m(a) {
                    return {
                        Pe: function (b) {
                            return a.Od[b] % 2 ? 1 : -1
                        }
                    }
                }

                function k(b, g, k, h, j) {
                    var d = i(b, g, k), e = 0;

                    function f(a) {
                        return c.B(1 - a / d, h)
                    }

                    if (b.Sd & 2) {
                        d = c.H(a / 2) - b.ed;
                        e = f(d - 1) / 2 * !b.ed
                    }
                    return {
                        Se: function (a) {
                            a = b.Le(a);
                            j && (a = d - a - 1);
                            return f(a) - e
                        }
                    }
                }

                j.Uf = e;
                j.Rf = function (o) {
                    var i = g[o];
                    if (!i) {
                        var h = e.p && e.p[o] || {}, y = b.wc(h.dl, .5), x = h.o || 0, z = h.r || 1, p = h.c, r = h.d,
                            n = b.wc(h.dO, 8), q = c.$Round(a * z), j = d(x), w = l(j, q, h.dlc, y),
                            t = p & 8 ? j : d(p), v = m(t), s = n & 8 ? j : d(n), u = k(s, q, h.dc, r, n == 9);
                        i = g[o] = {
                            nc: w.nc, Qf: function (a) {
                                return (p != f ? v.Pe(a) : 1) * (r ? u.Se(a) : 1)
                            }
                        }
                    }
                    return i
                }
            }

            var i = h(k), a = b.A(i), g = [];
            b.f(i, function (i, h) {
                var a = [], d = b.v({}, e), f = b.v({}, e, {o: j});
                b.f(n, function (j, n) {
                    var i = {}, o = {}, k = g[n] = g[n] || new l(j);
                    b.f(j, function (l, b) {
                        var n = k.Rf(b), p = n.nc(h);
                        if (p) {
                            var a, g = c.Y(l - d[b], 8);
                            if (g) {
                                g = c.Y(l - e[b], 8);
                                g *= n.Qf(h);
                                a = c.Y(g + e[b], 4);
                                var j = m[b];
                                if (j) {
                                    a = c.l(a, j.j);
                                    a = c.j(a, j.l)
                                }
                            } else a = l;
                            if (a - f[b]) {
                                i[b] = a;
                                o[b] = p
                            }
                        }
                    });
                    b.v(d, j);
                    b.v(f, i);
                    if (b.Th(i)) {
                        b.v(i, k.Uf);
                        i.dr = o;
                        a.push(i)
                    }
                });
                b.A(a) && o(i, a)
            })
        }
    };

    function p() {
        var a = this, f, e = [], c = [];

        function k(a, b) {
            e.push({ec: a, gc: b})
        }

        function j(a, c) {
            b.f(e, function (b, d) {
                b.ec == a && b.gc === c && e.splice(d, 1)
            })
        }

        function h() {
            e = []
        }

        function g() {
            b.f(c, function (a) {
                b.$RemoveEvent(a.Ne, a.ec, a.gc, a.Xe)
            });
            c = []
        }

        a.Oc = function () {
            return f
        };
        a.a = function (f, d, e, a) {
            b.$AddEvent(f, d, e, a);
            c.push({Ne: f, ec: d, gc: e, Xe: a})
        };
        a.T = function (f, d, e, a) {
            b.f(c, function (g, h) {
                if (g.Ne === f && g.ec == d && g.gc === e && g.Xe == a) {
                    b.$RemoveEvent(f, d, e, a);
                    c.splice(h, 1)
                }
            })
        };
        a.Ve = g;
        a.$On = a.addEventListener = k;
        a.$Off = a.removeEventListener = j;
        a.k = function (a) {
            var c = [].slice.call(arguments, 1);
            b.f(e, function (b) {
                b.ec == a && b.gc.apply(i, c)
            })
        };
        a.$Destroy = function () {
            if (!f) {
                f = d;
                g();
                h()
            }
        }
    }

    var l = function (C, F, l, m, L, M) {
        C = C || 0;
        var a = this, t, p, n, o, v, D = 0, O = 1, E, B = 0, h = 0, r = 0, A, j, e, g, u, z, s = [], I = k, J, H = k;

        function R(a) {
            e += a;
            g += a;
            j += a;
            h += a;
            r += a;
            B += a
        }

        function y(C) {
            var k = C;
            if (u) if (!z && (k >= g || k < e) || z && k >= e) k = ((k - e) % u + u) % u + e;
            if (!A || v || h != k) {
                var i = c.j(k, g);
                i = c.l(i, e);
                if (l.$Reverse) i = g - i + e;
                if (!A || v || i != r) {
                    if (t) {
                        var y = (i - j) / (F || 1), x = t(y), n;
                        if (J) {
                            var o = i > e && i < g;
                            if (o != H) n = H = o
                        }
                        if (!n && x != f) {
                            var p = !x;
                            if (p != I) n = I = p
                        }
                        if (n != f) {
                            n && b.lc(m, "none");
                            !n && b.lc(m, b.g(m, "data-events"))
                        }
                    }
                    var w = r, q = r = i;
                    b.f(s, function (c, d) {
                        var a = !A && z || k <= h ? s[b.A(s) - d - 1] : c;
                        a.L(i - B)
                    });
                    h = k;
                    A = d;
                    a.kd(w - j, q - j);
                    a.zc(w, q)
                }
            }
        }

        function G(a, b, d) {
            b && a.$Shift(g);
            if (!d) {
                e = c.j(e, a.yc() + B);
                g = c.l(g, a.vb() + B)
            }
            s.push(a)
        }

        var w = i.requestAnimationFrame || i.webkitRequestAnimationFrame || i.mozRequestAnimationFrame || i.msRequestAnimationFrame;
        if (b.He() && b.Cd() < 7 || !w) w = function (a) {
            b.$Delay(a, l.$Interval)
        };

        function N() {
            if (p) {
                var c = b.Tb(), d = c - D;
                D = c;
                var a = h + d * o * O;
                if (a * o >= n * o) a = n;
                y(a);
                if (!v && a * o >= n * o) P(E); else w(N)
            }
        }

        function x(f, i, j) {
            if (!p) {
                p = d;
                v = j;
                E = i;
                f = c.l(f, e);
                f = c.j(f, g);
                n = f;
                o = n < h ? -1 : 1;
                a.Qc();
                D = b.Tb();
                w(N)
            }
        }

        function P(b) {
            if (p) {
                v = p = E = k;
                a.Rc();
                b && b()
            }
        }

        a.$Play = function (a, b, c) {
            x(a ? h + a : g, b, c)
        };
        a.tc = x;
        a.Ff = function (a, b) {
            x(g, a, b)
        };
        a.S = P;
        a.Be = function () {
            return h
        };
        a.Ee = function () {
            return n
        };
        a.z = function () {
            return r
        };
        a.L = y;
        a.uf = function () {
            y(g, d)
        };
        a.$IsPlaying = function () {
            return p
        };
        a.De = function (a) {
            O = a
        };
        a.$Shift = R;
        a.je = G;
        a.M = function (a, b) {
            G(a, 0, b)
        };
        a.zd = function (a) {
            G(a, 1)
        };
        a.qd = function (a) {
            g += a
        };
        a.yc = function () {
            return e
        };
        a.vb = function () {
            return g
        };
        a.zc = a.Qc = a.Rc = a.kd = b.Kc;
        b.Tb();
        a.nf = function () {
            return t && t.E(1)
        };
        l = b.v({$Interval: 16}, l);
        m && (J = b.g(m, "data-inactive"));
        u = l.hc;
        z = l.pf;
        e = j = C;
        g = C + F;
        l.$Elmt = m;
        m && (t = b.Kf(L, M, l, d, d))
    };
    var u = i.$JssorSlideshowFormations$ = new function () {
        var i = this, e = 0, a = 1, g = 2, f = 3, t = 1, s = 2, u = 4, r = 8, x = 256, y = 512, w = 1024, v = 2048,
            k = v + t, j = v + s, p = y + t, n = y + s, o = x + u, l = x + r, m = w + u, q = w + r;

        function z(a) {
            return (a & s) == s
        }

        function A(a) {
            return (a & u) == u
        }

        function h(b, a, c) {
            c.push(a);
            b[a] = b[a] || [];
            b[a].push(c)
        }

        i.$FormationStraight = function (f) {
            for (var d = f.$Cols, e = f.$Rows, s = f.$Assembly, t = f.mc, r = [], a = 0, b = 0, i = d - 1, q = e - 1, g = t - 1, c, b = 0; b < e; b++) for (a = 0; a < d; a++) {
                switch (s) {
                    case k:
                        c = g - (a * e + (q - b));
                        break;
                    case m:
                        c = g - (b * d + (i - a));
                        break;
                    case p:
                        c = g - (a * e + b);
                    case o:
                        c = g - (b * d + a);
                        break;
                    case j:
                        c = a * e + b;
                        break;
                    case l:
                        c = b * d + (i - a);
                        break;
                    case n:
                        c = a * e + (q - b);
                        break;
                    default:
                        c = b * d + a
                }
                h(r, c, [b, a])
            }
            return r
        };
        i.$FormationSwirl = function (r) {
            var y = r.$Cols, z = r.$Rows, C = r.$Assembly, x = r.mc, B = [], A = [], v = 0, c = 0, i = 0, s = y - 1,
                t = z - 1, u, q, w = 0;
            switch (C) {
                case k:
                    c = s;
                    i = 0;
                    q = [g, a, f, e];
                    break;
                case m:
                    c = 0;
                    i = t;
                    q = [e, f, a, g];
                    break;
                case p:
                    c = s;
                    i = t;
                    q = [f, a, g, e];
                    break;
                case o:
                    c = s;
                    i = t;
                    q = [a, f, e, g];
                    break;
                case j:
                    c = 0;
                    i = 0;
                    q = [g, e, f, a];
                    break;
                case l:
                    c = s;
                    i = 0;
                    q = [a, g, e, f];
                    break;
                case n:
                    c = 0;
                    i = t;
                    q = [f, e, g, a];
                    break;
                default:
                    c = 0;
                    i = 0;
                    q = [e, g, a, f]
            }
            v = 0;
            while (v < x) {
                u = i + "," + c;
                if (c >= 0 && c < y && i >= 0 && i < z && !A[u]) {
                    A[u] = d;
                    h(B, v++, [i, c])
                } else switch (q[w++ % b.A(q)]) {
                    case e:
                        c--;
                        break;
                    case g:
                        i--;
                        break;
                    case a:
                        c++;
                        break;
                    case f:
                        i++
                }
                switch (q[w % b.A(q)]) {
                    case e:
                        c++;
                        break;
                    case g:
                        i++;
                        break;
                    case a:
                        c--;
                        break;
                    case f:
                        i--
                }
            }
            return B
        };
        i.$FormationZigZag = function (q) {
            var x = q.$Cols, y = q.$Rows, A = q.$Assembly, w = q.mc, u = [], v = 0, c = 0, d = 0, r = x - 1, s = y - 1,
                z, i, t = 0;
            switch (A) {
                case k:
                    c = r;
                    d = 0;
                    i = [g, a, f, a];
                    break;
                case m:
                    c = 0;
                    d = s;
                    i = [e, f, a, f];
                    break;
                case p:
                    c = r;
                    d = s;
                    i = [f, a, g, a];
                    break;
                case o:
                    c = r;
                    d = s;
                    i = [a, f, e, f];
                    break;
                case j:
                    c = 0;
                    d = 0;
                    i = [g, e, f, e];
                    break;
                case l:
                    c = r;
                    d = 0;
                    i = [a, g, e, g];
                    break;
                case n:
                    c = 0;
                    d = s;
                    i = [f, e, g, e];
                    break;
                default:
                    c = 0;
                    d = 0;
                    i = [e, g, a, g]
            }
            v = 0;
            while (v < w) {
                z = d + "," + c;
                if (c >= 0 && c < x && d >= 0 && d < y && typeof u[z] == "undefined") {
                    h(u, v++, [d, c]);
                    switch (i[t % b.A(i)]) {
                        case e:
                            c++;
                            break;
                        case g:
                            d++;
                            break;
                        case a:
                            c--;
                            break;
                        case f:
                            d--
                    }
                } else {
                    switch (i[t++ % b.A(i)]) {
                        case e:
                            c--;
                            break;
                        case g:
                            d--;
                            break;
                        case a:
                            c++;
                            break;
                        case f:
                            d++
                    }
                    switch (i[t++ % b.A(i)]) {
                        case e:
                            c++;
                            break;
                        case g:
                            d++;
                            break;
                        case a:
                            c--;
                            break;
                        case f:
                            d--
                    }
                }
            }
            return u
        };
        i.$FormationStraightStairs = function (i) {
            var u = i.$Cols, v = i.$Rows, e = i.$Assembly, t = i.mc, r = [], s = 0, c = 0, d = 0, f = u - 1, g = v - 1,
                x = t - 1;
            switch (e) {
                case k:
                case n:
                case p:
                case j:
                    var a = 0, b = 0;
                    break;
                case l:
                case m:
                case o:
                case q:
                    var a = f, b = 0;
                    break;
                default:
                    e = q;
                    var a = f, b = 0
            }
            c = a;
            d = b;
            while (s < t) {
                if (A(e) || z(e)) h(r, x - s++, [d, c]); else h(r, s++, [d, c]);
                switch (e) {
                    case k:
                    case n:
                        c--;
                        d++;
                        break;
                    case p:
                    case j:
                        c++;
                        d--;
                        break;
                    case l:
                    case m:
                        c--;
                        d--;
                        break;
                    case q:
                    case o:
                    default:
                        c++;
                        d++
                }
                if (c < 0 || d < 0 || c > f || d > g) {
                    switch (e) {
                        case k:
                        case n:
                            a++;
                            break;
                        case l:
                        case m:
                        case p:
                        case j:
                            b++;
                            break;
                        case q:
                        case o:
                        default:
                            a--
                    }
                    if (a < 0 || b < 0 || a > f || b > g) {
                        switch (e) {
                            case k:
                            case n:
                                a = f;
                                b++;
                                break;
                            case p:
                            case j:
                                b = g;
                                a++;
                                break;
                            case l:
                            case m:
                                b = g;
                                a--;
                                break;
                            case q:
                            case o:
                            default:
                                a = 0;
                                b++
                        }
                        if (b > g) b = g; else if (b < 0) b = 0; else if (a > f) a = f; else if (a < 0) a = 0
                    }
                    d = b;
                    c = a
                }
            }
            return r
        };
        i.$FormationRectangle = function (f) {
            var d = f.$Cols || 1, e = f.$Rows || 1, g = [], a, b, i;
            i = c.$Round(c.j(d / 2, e / 2)) + 1;
            for (a = 0; a < d; a++) for (b = 0; b < e; b++) h(g, i - c.j(a + 1, b + 1, d - a, e - b), [b, a]);
            return g
        };
        i.$FormationRandom = function (d) {
            for (var e = [], a, b = 0; b < d.$Rows; b++) for (a = 0; a < d.$Cols; a++) h(e, c.H(1e5 * c.dd()) % 13, [b, a]);
            return e
        };
        i.$FormationCircle = function (d) {
            for (var e = d.$Cols || 1, f = d.$Rows || 1, g = [], a, i = e / 2 - .5, j = f / 2 - .5, b = 0; b < e; b++) for (a = 0; a < f; a++) h(g, c.$Round(c.xb(c.B(b - i, 2) + c.B(a - j, 2))), [a, b]);
            return g
        };
        i.$FormationCross = function (d) {
            for (var e = d.$Cols || 1, f = d.$Rows || 1, g = [], a, i = e / 2 - .5, j = f / 2 - .5, b = 0; b < e; b++) for (a = 0; a < f; a++) h(g, c.$Round(c.j(c.P(b - i), c.P(a - j))), [a, b]);
            return g
        };
        i.$FormationRectangleCross = function (f) {
            for (var g = f.$Cols || 1, i = f.$Rows || 1, j = [], a, d = g / 2 - .5, e = i / 2 - .5, k = c.l(d, e) + 1, b = 0; b < g; b++) for (a = 0; a < i; a++) h(j, c.$Round(k - c.l(d - c.P(b - d), e - c.P(a - e))) - 1, [a, b]);
            return j
        }
    };
    i.$JssorSlideshowRunner$ = function (n, q, o, r, w, v) {
        var a = this, f, m, i, t = 0, s = r.$TransitionsOrder;

        function h(a) {
            var c = {
                $Left: "x",
                $Top: "y",
                $Bottom: "m",
                $Right: "t",
                $Rotate: "r",
                $ScaleX: "sX",
                $ScaleY: "sY",
                $TranslateX: "tX",
                $TranslateY: "tY",
                $SkewX: "kX",
                $SkewY: "kY",
                $Opacity: "o",
                $ZIndex: "i",
                $Clip: "c"
            };
            b.f(a, function (e, d) {
                var b = c[d];
                if (b) {
                    a[b] = e;
                    delete a[d];
                    b == "c" && h(e)
                }
            });
            if (a.$Zoom) a.sX = a.sY = a.$Zoom
        }

        function j(f, e) {
            var a = {
                $Duration: 1,
                $Delay: 0,
                $Cols: 1,
                $Rows: 1,
                $Opacity: 0,
                $Zoom: 0,
                $Clip: 0,
                $Move: k,
                $SlideOut: k,
                $Reverse: k,
                $Formation: u.$FormationRandom,
                $Assembly: 1032,
                $ChessMode: {$Column: 0, $Row: 0},
                $Easing: g.$Linear,
                $Round: {},
                Ic: [],
                $During: {}
            };
            b.v(a, f);
            if (a.$Rows == 0) a.$Rows = c.$Round(a.$Cols * e);
            a.$Easing = b.Ld(a.$Easing);
            h(a);
            h(a.$Easing);
            h(a.$During);
            h(a.$Round);
            a.mc = a.$Cols * a.$Rows;
            a.Af = function (c, b) {
                c /= a.$Cols;
                b /= a.$Rows;
                var f = c + "x" + b;
                if (!a.Ic[f]) {
                    a.Ic[f] = {w: c, h: b};
                    for (var d = 0; d < a.$Cols; d++) for (var e = 0; e < a.$Rows; e++) a.Ic[f][e + "," + d] = {
                        y: e * b,
                        t: d * c + c,
                        m: e * b + b,
                        x: d * c
                    }
                }
                return a.Ic[f]
            };
            if (a.$Brother) {
                a.$Brother = j(a.$Brother, e);
                a.$SlideOut = d
            }
            return a
        }

        function p(s, g, a, t, o, n) {
            var h, e, j = a.$ChessMode.$Column || 0, m = a.$ChessMode.$Row || 0, i = a.Af(o, n), p = a.$Formation(a),
                r = a.$SlideOut;
            g = b.ab(g);
            b.N(g, 1);
            b.Fb(g, "hidden");
            b.db(g, "absolute");
            v(g, 0, 0);
            !a.$Reverse && p.reverse();
            var f = {x: a.c & 1, t: a.c & 2, y: a.c & 4, m: a.c & 8}, q = new l(0, 0);
            b.f(p, function (w, v) {
                if (r) v = b.A(p) - v - 1;
                var x = a.$Delay * v;
                b.f(w, function (G) {
                    var J = G[0], I = G[1], O = J + "," + I, v = k, w = k, z = k;
                    if (j && I % 2) {
                        if (j & 3) v = !v;
                        if (j & 12) w = !w;
                        if (j & 16) z = !z
                    }
                    if (m && J % 2) {
                        if (m & 3) v = !v;
                        if (m & 12) w = !w;
                        if (m & 16) z = !z
                    }
                    var E = w ? f.m : f.y, B = w ? f.y : f.m, D = v ? f.t : f.x, C = v ? f.x : f.t,
                        H = E || B || D || C, A = b.ab(g);
                    e = {x: 0, y: 0, o: 1};
                    h = b.v({}, e);
                    if (a.o) e.o = 2 - a.o;
                    var N = a.$Cols * a.$Rows > 1 || H;
                    if (a.sX || a.r) {
                        var M = d;
                        if (M) {
                            e.sX = e.sY = a.sX ? a.sX - 1 : 1;
                            h.sX = h.sY = 1;
                            var T = a.r || 0;
                            e.r = T * 360 * (z ? -1 : 1);
                            h.r = 0
                        }
                    }
                    if (N) {
                        var F = i[O];
                        if (H) {
                            var p = {}, y = a.$ScaleClip || 1;
                            if (E && B) {
                                p.y = i.h / 2 * y;
                                p.m = -p.y
                            } else if (E) p.m = -i.h * y; else if (B) p.y = i.h * y;
                            if (D && C) {
                                p.x = i.w / 2 * y;
                                p.t = -p.x
                            } else if (D) p.t = -i.w * y; else if (C) p.x = i.w * y;
                            if (a.$Move) {
                                var R = (p.x || 0) + (p.t || 0), S = (p.y || 0) + (p.m || 0);
                                e.x += R;
                                e.y += S
                            }
                            h.c = F;
                            b.f(p, function (b, a) {
                                p[a] = F[a] + b
                            });
                            e.c = p
                        } else b.kh(A, F)
                    }
                    var P = v ? 1 : -1, Q = w ? 1 : -1;
                    if (a.x) e.x += o * a.x * P;
                    if (a.y) e.y += n * a.y * Q;
                    var K = {
                        $Elmt: A,
                        $Easing: a.$Easing,
                        $During: a.$During,
                        $Round: a.$Round,
                        $Move: a.$Move,
                        Eb: o,
                        Gb: n,
                        le: c.$Round(a.$Duration / 4),
                        $Reverse: !r
                    };
                    e = b.Zg(e, h);
                    var L = new l(t + x, a.$Duration, K, A, h, e);
                    q.M(L);
                    s.Ef(A)
                })
            });
            q.L(-1);
            return q
        }

        a.Bf = function () {
            var a = 0, d = r.$Transitions, e = b.A(d);
            if (s) a = t++ % e; else a = c.G(c.dd() * e);
            d[a] && (d[a].Qb = a);
            return d[a]
        };
        a.Ob = function () {
            n.Ob();
            m = e;
            i = e
        };
        a.Cf = function (v, y, w, x, s, k) {
            f = j(s, k);
            var h = x.Re, d = w.Re, e = h, g = d, r = f, b = f.$Brother || j({}, k);
            if (!f.$SlideOut) {
                e = d;
                g = h
            }
            var l = b.$Shift || 0, u = c.l(l, 0), t = c.l(-l, 0);
            m = p(n, g, b, u, q, o);
            i = p(n, e, r, t, q, o);
            a.Qb = v
        };
        a.of = function () {
            var a = e;
            if (i) {
                a = new l(0, 0);
                a.M(i);
                a.M(m);
                a.ye = f
            }
            return a
        }
    };
    var o = {qf: "data-scale", yb: "data-autocenter", Dd: "data-nofreeze", ze: "data-nodrag"}, q = new function () {
        var a = this;
        a.Ac = function (c, a, e, d) {
            (d || !b.g(c, a)) && b.g(c, a, e)
        };
        a.Cc = function (a) {
            var c = b.q(a, o.yb);
            b.Uc(a, c)
        }
    }, s = {uc: 1};
    i.$JssorBulletNavigator$ = function () {
        var a = this, E = b.W(a, p), h, v, C, B, m, l = 0, g, r, n, z, A, i, k, u, t, x, j;

        function y(a) {
            j[a] && j[a].Ye(a == l)
        }

        function w(b) {
            a.k(s.uc, b * r)
        }

        a.Sc = function (a) {
            if (a != m) {
                var d = l, b = c.G(a / r);
                l = b;
                m = a;
                y(d);
                y(b)
            }
        };
        a.id = function (a) {
            b.mb(h, !a)
        };
        a.nd = function (J) {
            b.$Destroy(j);
            m = f;
            a.Ve();
            x = [];
            j = [];
            b.Rb(h);
            v = c.H(J / r);
            l = 0;
            var F = u + z, G = t + A, s = c.H(v / n) - 1;
            C = u + F * (!i ? s : n - 1);
            B = t + G * (i ? s : n - 1);
            b.K(h, C);
            b.J(h, B);
            for (var o = 0; o < v; o++) {
                var H = b.Rd();
                b.bd(H, o + 1);
                var p = b.Ce(k, "numbertemplate", H, d);
                b.db(p, "absolute");
                var E = o % (s + 1), I = c.G(o / (s + 1)), y = g.Yb && !i ? s - E : E;
                b.U(p, (!i ? y : I) * F);
                b.V(p, (i ? y : I) * G);
                b.O(h, p);
                x[o] = p;
                g.$ActionMode & 1 && a.a(p, "click", b.Z(e, w, o));
                g.$ActionMode & 2 && a.a(p, "mouseenter", b.Z(e, w, o));
                j[o] = b.Lc(p)
            }
            q.Cc(h)
        };
        a.F = function (d, c) {
            a.$Elmt = h = b.$GetElement(d);
            a.gd = g = b.v({$SpacingX: 10, $SpacingY: 10, $ActionMode: 1}, c);
            k = b.$FindChild(h, "prototype");
            u = b.K(k);
            t = b.J(k);
            b.ib(k, h);
            r = g.$Steps || 1;
            n = g.$Rows || 1;
            z = g.$SpacingX;
            A = g.$SpacingY;
            i = g.$Orientation & 2;
            g.$AutoCenter && q.Ac(h, o.yb, g.$AutoCenter)
        };
        a.$Destroy = function () {
            b.$Destroy(j, E)
        };
        b.F(a)
    };
    i.$JssorArrowNavigator$ = function () {
        var a = this, v = b.W(a, p), f, c, g, l, r, k, h, m, j, i;

        function n(b) {
            a.k(s.uc, b, d)
        }

        function u(a) {
            b.mb(f, !a);
            b.mb(c, !a)
        }

        function t() {
            j.$Enable((g.$Loop || !l.lf(h)) && k > 1);
            i.$Enable((g.$Loop || !l.ef(h)) && k > 1)
        }

        a.Sc = function (c, a, b) {
            h = a;
            !b && t()
        };
        a.id = u;
        a.nd = function (g) {
            k = g;
            h = 0;
            if (!r) {
                a.a(f, "click", b.Z(e, n, -m));
                a.a(c, "click", b.Z(e, n, m));
                j = b.Lc(f);
                i = b.Lc(c);
                b.g(f, o.Dd, 1);
                b.g(c, o.Dd, 1);
                r = d
            }
        };
        a.F = function (e, d, h, i) {
            a.gd = g = b.v({$Steps: 1}, h);
            f = e;
            c = d;
            if (g.Yb) {
                f = d;
                c = e
            }
            m = g.$Steps;
            l = i;
            if (g.$AutoCenter) {
                q.Ac(f, o.yb, g.$AutoCenter);
                q.Ac(c, o.yb, g.$AutoCenter)
            }
            q.Cc(f);
            q.Cc(c)
        };
        a.$Destroy = function () {
            b.$Destroy(j, i, v)
        };
        b.F(a)
    };
    i.$JssorThumbnailNavigator$ = function () {
        var i = this, E = b.W(i, p), h, B, a, y, C, m, l = [], A, z, g, n, r, w, v, x, t, u;

        function D() {
            var c = this;
            b.W(c, p);
            var h, f, n, l;

            function o() {
                n.Ye(m == h)
            }

            function j(e) {
                if (e || !t.$LastDragSucceeded()) {
                    var c = g - h % g, a = t.Id((h + c) / g - 1), b = a * g + g - c;
                    if (a < 0) b += y % g;
                    if (a >= C) b -= y % g;
                    i.k(s.uc, b, k, d)
                }
            }

            c.Hd = o;
            c.F = function (g, i) {
                c.Qb = h = i;
                l = g.nh || g.ih || b.bc();
                c.Wc = f = b.Ce(u, "thumbnailtemplate", l, d);
                n = b.Lc(f);
                a.$ActionMode & 1 && c.a(f, "click", b.Z(e, j, 0));
                a.$ActionMode & 2 && c.a(f, "mouseenter", b.Z(e, j, 1))
            };
            b.F(c)
        }

        i.Sc = function (a, e, d) {
            if (a != m) {
                var b = m;
                m = a;
                b != -1 && l[b].Hd();
                l[a] && l[a].Hd()
            }
            !d && t.$PlayTo(t.Id(c.G(a / g)))
        };
        i.id = function (a) {
            b.mb(h, !a)
        };
        i.nd = function (I, J) {
            b.$Destroy(t, l);
            m = f;
            l = [];
            var K = b.ab(B);
            b.Rb(h);
            a.Yb && b.g(h, "dir", "rtl");
            b.ph(h, b.jb(K));
            var i = b.$FindChild(h, "slides", d);
            y = I;
            C = c.H(y / g);
            m = -1;
            var e = a.$Orientation & 1, s = w + (w + n) * (g - 1) * (1 - e), p = v + (v + r) * (g - 1) * e,
                E = (e ? c.l : c.j)(A, s), u = (e ? c.j : c.l)(z, p);
            x = c.H((A - n) / (w + n) * e + (z - r) / (v + r) * (1 - e));
            var G = s + (s + n) * (x - 1) * e, F = p + (p + r) * (x - 1) * (1 - e);
            E = c.j(E, G);
            u = c.j(u, F);
            b.K(i, E);
            b.J(i, u);
            b.Uc(i, 3);
            var o = [];
            b.f(J, function (k, f) {
                var h = new D(k, f), d = h.Wc, a = c.G(f / g), j = f % g;
                b.U(d, (w + n) * j * (1 - e));
                b.V(d, (v + r) * j * e);
                if (!o[a]) {
                    o[a] = b.bc();
                    b.O(i, o[a])
                }
                b.O(o[a], d);
                l.push(h)
            });
            var H = b.v({
                $AutoPlay: 0,
                $NaviQuitDrag: k,
                $SlideWidth: s,
                $SlideHeight: p,
                $SlideSpacing: n * e + r * (1 - e),
                $MinDragOffsetToSlide: 12,
                $SlideDuration: 200,
                $PauseOnHover: 1,
                $Cols: x,
                $PlayOrientation: a.$Orientation,
                $DragOrientation: a.$NoDrag || a.$DisableDrag ? 0 : a.$Orientation
            }, a);
            t = new j(h, H);
            q.Cc(h)
        };
        i.F = function (j, f, e) {
            h = j;
            i.gd = a = b.v({$SpacingX: 0, $SpacingY: 0, $Orientation: 1, $ActionMode: 1}, f);
            A = b.K(h);
            z = b.J(h);
            var c = b.$FindChild(h, "slides", d);
            u = b.$FindChild(c, "prototype");
            e = b.ab(e);
            b.pb(e, c);
            w = b.K(u);
            v = b.J(u);
            b.ib(u, c);
            b.db(c, "absolute");
            b.Fb(c, "hidden");
            g = a.$Rows || 1;
            n = a.$SpacingX;
            r = a.$SpacingY;
            a.$AutoCenter &= a.$Orientation;
            a.$AutoCenter && q.Ac(h, o.yb, a.$AutoCenter);
            B = b.ab(h)
        };
        i.$Destroy = function () {
            b.$Destroy(t, l, E)
        };
        b.F(i)
    };

    function n(e, d, c) {
        var a = this;
        b.W(a, p);
        l.call(a, 0, c.$Idle);
        a.qc = 0;
        a.fd = c.$Idle
    }

    n.pc = 21;
    n.Zb = 24;
    var t = i.$JssorCaptionSlideo$ = function () {
        var a = this, db = b.W(a, p);
        l.call(a, 0, 0);
        var f, j, B, C, w = new l(0, 0), L = [], u = [], F, q = 0;

        function H(c, f) {
            var a = L[c];
            if (a == e) {
                a = L[c] = {ob: c, Zc: [], Te: []};
                var d = 0;
                !b.f(u, function (a, b) {
                    d = b;
                    return a.ob > c
                }) && d++;
                u.splice(d, 0, a)
            }
            return a
        }

        function Q(f, v) {
            var s = b.K(f), r = b.J(f), m = b.Ib(f), j = {
                x: m ? 0 : b.U(f),
                y: m ? 0 : b.V(f),
                cc: 0,
                Wb: 0,
                o: b.cb(f),
                i: b.N(f) || 0,
                r: 0,
                rX: 0,
                rY: 0,
                sX: 1,
                sY: 1,
                tX: 0,
                tY: 0,
                tZ: 0,
                kX: 0,
                kY: 0,
                ls: 0,
                lh: 1,
                so: 0,
                c: {y: 0, t: s, m: r, x: 0}
            }, a, g;
            if (C) {
                var o = C[b.q(f, "c")];
                if (o) {
                    a = H(o.r, 0);
                    a.sg = o.e || 0
                }
            }
            var h = b.g(f, "data-to");
            if (h && m) {
                h = b.Ud(h);
                h = {x: b.od(h[0]), y: b.od(h[1])}
            }
            var u = {$Elmt: f, $OriginalWidth: s, $OriginalHeight: r, Nf: h, Lf: j.x, Of: j.y, Ib: m};
            b.f(v, function (e) {
                var m = b.v({$Easing: b.Ld(e.e), $During: e.dr, Bd: e.p}, u), i = b.v(d, {}, e);
                b.Pd(i, ["b", "d", "e", "p", "dr"]);
                var h = new l(e.b, e.d, m, f, j, i);
                q = c.l(q, e.b + e.d);
                if (a) {
                    if (!g) g = new l(e.b, 0);
                    g.M(h)
                } else {
                    var k = H(e.b, e.b + e.d);
                    k.Zc.push(h)
                }
                j = h.nf()
            });
            if (a && g) {
                g.uf();
                var i = g, n, k = g.yc(), p = g.vb(), t = c.l(p, a.sg);
                if (a.ob < p) {
                    if (a.ob > k) {
                        i = new l(k, a.ob - k);
                        i.M(g, d)
                    } else i = e;
                    n = new l(a.ob, t - k, {hc: t - a.ob, pf: d});
                    n.M(g, d)
                }
                i && a.Zc.push(i);
                n && a.Te.push(n)
            }
            return j
        }

        function N(d, c) {
            b.f(d, function (d) {
                var f = b.q(d, "play");
                if (c && f) {
                    var e = new t(d, j, {xe: f});
                    E.push(e);
                    a.a(e, n.pc, I);
                    a.a(e, n.Zb, G)
                } else {
                    N(b.jb(d).concat(b.xc(b.Hc(d, "data-tchd"))), c + 1);
                    var g = b.xc(b.Hc(d, "data-tsep"));
                    g.push(d);
                    b.f(g, function (c) {
                        var a = B[b.q(c, "t")];
                        a && Q(c, a)
                    })
                }
            })
        }

        function cb(f, e, g) {
            var c = f.b - e;
            if (c) {
                var b = new l(e, c);
                b.M(w, d);
                b.$Shift(g);
                a.M(b)
            }
            a.qd(f.d);
            return c
        }

        function bb(e) {
            var c = w.yc(), d = 0;
            b.f(e, function (e, f) {
                e = b.v({d: 3e3}, e);
                cb(e, c, d);
                c = e.b;
                d += e.d;
                if (!f || e.t == 2) {
                    a.qc = c;
                    a.fd = c + e.d
                }
            })
        }

        function A(i, d, e) {
            var f = b.A(d);
            if (f > 4) for (var j = c.H(f / 4), a = 0; a < j; a++) {
                var g = d.slice(a * 4, c.j(a * 4 + 4, f)), h = new l(g[0].ob, 0);
                A(h, g, e);
                i.M(h)
            } else b.f(d, function (a) {
                b.f(e ? a.Te : a.Zc, function (a) {
                    e && a.qd(q - a.vb());
                    i.M(a)
                })
            })
        }

        var i, M, y = 0, g, x, S, R, z, E = [], O = [], r, D, m;

        function v(a) {
            return a & 2 || a & 4 && b.ud().td
        }

        function Z() {
            if (!z) {
                g & 8 && a.a(h, "keydown", J);
                if (g & 32) {
                    a.a(h, "mousedown", s);
                    a.a(h, "touchstart", s)
                }
                z = d
            }
        }

        function Y() {
            a.T(h, "keydown", J);
            a.T(h, "mousedown", s);
            a.T(h, "touchstart", s);
            z = k
        }

        function T(b) {
            if (!r || b) {
                r = d;
                a.S();
                b && y && a.L(0);
                a.De(1);
                a.Ff();
                Z();
                a.k(n.pc, a)
            }
        }

        function o() {
            if (!D && (r || a.z())) {
                D = d;
                a.S();
                a.Be() > a.qc && a.L(a.qc);
                a.De(S || 1);
                a.tc(0)
            }
        }

        function V() {
            !m && o()
        }

        function U(c) {
            var b = c;
            if (c < 0 && a.z()) b = 1;
            if (b != y) {
                y = b;
                M && a.k(n.Zb, a, y)
            }
        }

        function J(a) {
            g & 8 && b.Je(a) == 27 && o()
        }

        function X(a) {
            if (m && b.Fe(a) !== e) {
                m = k;
                g & 16 && b.$Delay(V, 160)
            }
        }

        function s(a) {
            g & 32 && !b.Ae(f, b.$EvtSrc(a)) && o()
        }

        function W(a) {
            if (!m) {
                m = d;
                if (i & 1) b.Ie(a, f) && T()
            }
        }

        function ab(j) {
            var h = b.$EvtSrc(j), a = b.kb(h, e, e, "A"), c = a && (b.qe(a) || a === f || b.Ae(f, a));
            if (r && v(g)) !c && o(); else if (v(i)) !c && T(d)
        }

        function I(b) {
            var c = b.wg(), a = O[c];
            a !== b && a && a.vg();
            O[c] = b
        }

        function G(b, c) {
            a.k(n.Zb, b, c)
        }

        a.wg = function () {
            return R || ""
        };
        a.vg = o;
        a.Qc = function () {
            U(1)
        };
        a.Rc = function () {
            r = k;
            D = k;
            U(-1);
            !a.z() && Y()
        };
        a.zc = function () {
            !m && x && a.Be() > a.fd && o()
        };
        a.F = function (m, k, e) {
            f = m;
            j = k;
            i = e.xe;
            F = e.cg;
            B = j.$Transitions;
            C = j.$Controls;
            N([f], 0);
            A(w, u);
            if (i) {
                a.M(w);
                F = d;
                x = b.q(f, "idle");
                g = b.q(f, "rollback");
                S = b.q(f, "speed", 1);
                R = b.hb(f, "group");
                (v(i) || v(g)) && a.a(f, "click", ab);
                if ((i & 1 || x) && !b.ud().td) {
                    a.a(f, "mouseenter", W);
                    a.a(f, "mouseleave", X)
                }
                M = b.q(f, "pause")
            }
            var l = j.$Breaks || [], c = l[b.q(f, "b")] || [], h = {b: q, d: b.A(c) ? 0 : e.$Idle || x || 0};
            c = c.concat([h]);
            bb(c);
            a.vb();
            F && a.qd(1e8);
            q = a.vb();
            A(a, u, d);
            a.L(-1);
            a.L(b.q(f, "initial") || 0)
        };
        a.$Destroy = function () {
            b.$Destroy(db, E);
            a.S();
            a.L(-1)
        };
        b.F(a)
    }, j = i.$JssorSlider$ = (i.module || {}).exports = function () {
        var a = this, Gc = b.W(a, p), Ob = "data-jssor-slider", ic = "data-jssor-thumb", u, m, S, Cb, kb, jb, X, J, O,
            M, Zb, Cc, Hc = 1, Bc = 1, kc = 1, sc = 1, nc = {}, w, R, Mb, bc, Yb, wb, zb, yb, ab, H = [], Rb, r = -1,
            tc, q, I, G, P, ob, pb, E, N, lb, T, z, W, nb, Z = [], vc, xc, oc, t, vb, Hb, qb, eb, Y, Kb, Gb, Qb, Sb, F,
            Lb = 0, cb = 0, Q = Number.MAX_VALUE, K = Number.MIN_VALUE, C, mb, db, U = 1, Xb = 0, fb, y, Fb, Eb, L, Ab,
            Db, B, V, rb, A, Bb, cc = b.ud(), Vb = cc.td, x = [], D, hb, bb, Nb, hc, mc, ib;

        function Jb() {
            return !U && Y & 12
        }

        function Ic() {
            return Xb || !U && Y & 3
        }

        function Ib() {
            return !y && !Jb() && !A.$IsPlaying()
        }

        function Wc() {
            return !Ic() && Ib()
        }

        function jc() {
            return z || S
        }

        function Pc() {
            return jc() & 2 ? pb : ob
        }

        function lc(a, c, d) {
            b.U(a, c);
            b.V(a, d)
        }

        function Fc(c, b) {
            var a = jc(), d = (ob * b + Lb) * (a & 1), e = (pb * b + Lb) * (a & 2) / 2;
            lc(c, d, e)
        }

        function dc(b, f) {
            if (y && !(C & 1)) {
                var e = b, d;
                if (b < K) {
                    e = K;
                    d = -1
                }
                if (b > Q) {
                    e = Q;
                    d = 1
                }
                if (d) {
                    var a = b - e;
                    if (f) {
                        a = c.Xf(a) * 2 / c.u;
                        a = c.B(a * d, 1.6)
                    } else {
                        a = c.B(a * d, .625);
                        a = c.Oe(a * c.u / 2)
                    }
                    b = e + a * d
                }
            }
            return b
        }

        function qc(a) {
            return dc(a, d)
        }

        function Nc(a) {
            return dc(a)
        }

        function xb(a, b) {
            if (!(C & 1)) {
                var c = a - Q + (b || 0), d = K - a + (b || 0);
                if (c > 0 && c > d) a = Q; else if (d > 0) a = K
            }
            return a
        }

        function yc(a) {
            return !(C & 1) && a - K < .0001
        }

        function wc(a) {
            return !(C & 1) && Q - a < .0001
        }

        function sb(a) {
            return !(C & 1) && (a - K < .0001 || Q - a < .0001)
        }

        function Tb(c, a, d) {
            !ib && b.f(Z, function (b) {
                b.Sc(c, a, d)
            })
        }

        function ec(b) {
            var a = b, d = sb(b);
            if (d) a = xb(a); else {
                b = v(b);
                a = b
            }
            a = c.G(a);
            a = c.l(a, 0);
            return a
        }

        function fd(a) {
            x[r];
            Rb = r;
            r = a;
            tc = x[r]
        }

        function zc() {
            z = 0;
            var b = B.z(), d = ec(b);
            Tb(d, b);
            if (sb(b) || b == c.G(b)) {
                if (t & 2 && (eb > 0 && d == q - 1 || eb < 0 && !d)) t = 0;
                fd(d);
                a.k(j.$EVT_PARK, r, Rb)
            }
        }

        function pc(a, b) {
            if (q && (!b || !A.$IsPlaying())) {
                A.S();
                realPosition = qc(a);
                V.L(realPosition);
                zc()
            }
        }

        function ub(a) {
            if (q) {
                a = xb(a);
                a = v(a);
                fb = k;
                _IsStandBy = k;
                y = k;
                pc(a)
            } else Tb(0, 0)
        }

        function Zc() {
            var b = j.Ke || 0, a = mb;
            j.Ke |= a;
            return W = a & ~b
        }

        function Uc() {
            if (W) {
                j.Ke &= ~mb;
                W = 0
            }
        }

        function Dc(c) {
            var a = b.bc();
            b.rb(a, ab);
            c && b.Fb(a, "hidden");
            return a
        }

        function v(b, a) {
            a = a || q || 1;
            return (b % a + a) % a
        }

        function fc(c, a, b) {
            t & 8 && (t = 0);
            tb(c, Gb, a, b)
        }

        function Ub() {
            b.f(Z, function (a) {
                a.id(a.gd.$ChanceToShow <= U)
            })
        }

        function Mc(c) {
            if (!U && (b.Fe(c) || !b.Ie(c, u))) {
                U = 1;
                Ub();
                if (!y) {
                    Y & 12 && Jc();
                    x[r] && x[r].Bc()
                }
                a.k(j.$EVT_MOUSE_LEAVE)
            }
        }

        function Lc() {
            if (U) {
                U = 0;
                Ub();
                y || !(Y & 12) || Kc()
            }
            a.k(j.$EVT_MOUSE_ENTER)
        }

        function Wb(b, a) {
            tb(b, a, d)
        }

        function tb(g, h, l, p) {
            if (q && (!y || m.$NaviQuitDrag) && !Jb() && !isNaN(g)) {
                var e = B.z(), a = g;
                if (l) {
                    a = e + g;
                    if (C & 2) {
                        if (yc(e) && g < 0) a = Q;
                        if (wc(e) && g > 0) a = K
                    }
                }
                if (!(C & 1)) if (p) a = v(a); else a = xb(a, .5);
                if (l && !sb(a)) a = c.$Round(a);
                var i = (a - e) % q;
                a = e + i;
                if (h == f) h = Gb;
                var b = c.P(i), j = 0;
                if (b) {
                    if (b < 1) b = c.B(b, .5);
                    if (b > 1) {
                        var o = Pc(), n = (S & 1 ? zb : yb) / o;
                        b = c.j(b, n * 1.5)
                    }
                    j = h * b
                }
                ib = d;
                A.S();
                ib = k;
                A.se(e, a, j)
            }
        }

        function Rc(e, h, n) {
            var l = this, i = {$Top: 2, $Right: 1, $Bottom: 2, $Left: 1},
                m = {$Top: "top", $Right: "right", $Bottom: "bottom", $Left: "left"}, g, a, f, j, k = {};
            l.$Elmt = e;
            l.$ScaleSize = function (q, p, t) {
                var l, s = q, r = p;
                if (!f) {
                    f = b.Ch(e);
                    g = e.parentNode;
                    j = {$Scale: b.q(e, o.qf, 1), $AutoCenter: b.q(e, o.yb)};
                    b.f(m, function (c, a) {
                        k[a] = b.q(e, "data-scale-" + c, 1)
                    });
                    a = e;
                    if (h) {
                        a = b.ab(g, d);
                        b.rb(a, {$Top: 0, $Left: 0});
                        b.O(a, e);
                        b.O(g, a)
                    }
                }
                if (n) {
                    l = c.l(q, p);
                    if (h) if (t >= 0 && t < 1) {
                        var v = c.j(q, p);
                        l = c.j(l / v, 1 / (1 - t)) * v
                    }
                } else s = r = l = c.B(O < M ? p : q, j.$Scale);
                l *= h && (l != 1 || b.He()) ? 1.001 : 1;
                h && (sc = l);
                b.we(a, l);
                b.K(g, f.Eb * s);
                b.J(g, f.Gb * r);
                var u = b.ue() && b.Cd() < 9 ? l : 1, w = (s - u) * f.Eb / 2, x = (r - u) * f.Gb / 2;
                b.U(a, w);
                b.V(a, x);
                b.f(f, function (d, a) {
                    if (i[a] && d) {
                        var e = (i[a] & 1) * c.B(q, k[a]) * d + (i[a] & 2) * c.B(p, k[a]) * d / 2;
                        b.If[a](g, e)
                    }
                });
                b.Uc(g, j.$AutoCenter)
            }
        }

        function dd() {
            var a = this;
            l.call(a, 0, 0, {hc: q});
            b.f(x, function (b) {
                a.zd(b);
                b.$Shift(F / E)
            })
        }

        function cd() {
            var a = this, b = Bb.$Elmt;
            l.call(a, -1, 2, {$Easing: g.$Linear, Pc: {Pb: Fc}, hc: q, $Reverse: Hb}, b, {Pb: 1}, {Pb: -1});
            a.Wc = b
        }

        function ed() {
            var b = this;
            l.call(b, -1e8, 2e8);
            b.zc = function (e, b) {
                if (c.P(b - e) > 1e-5) {
                    var g = b, f = b;
                    if (c.G(b) != b && b > e && (C & 1 || b > cb)) f++;
                    var h = ec(f);
                    Tb(h, g, d);
                    a.k(j.$EVT_POSITION_CHANGE, v(g), v(e), b, e)
                }
            }
        }

        function Tc(o, n) {
            var b = this, g, i, f, c, h;
            l.call(b, -1e8, 2e8, {});
            b.Qc = function () {
                fb = d;
                a.k(j.$EVT_SWIPE_START, v(B.z()), V.z())
            };
            b.Rc = function () {
                fb = k;
                c = k;
                a.k(j.$EVT_SWIPE_END, v(B.z()), V.z());
                !y && zc()
            };
            b.zc = function (e, b) {
                var a = b;
                if (c) a = h; else if (f) {
                    var d = b / f;
                    a = m.$SlideEasing(d) * (i - g) + g
                }
                a = qc(a);
                V.L(a)
            };
            b.se = function (a, c, h, e) {
                y = k;
                f = h || 1;
                g = a;
                i = c;
                ib = d;
                V.L(a);
                ib = k;
                b.L(0);
                b.tc(f, e)
            };
            b.Ng = function () {
                c = d;
                c && b.$Play(e, e, d)
            };
            b.Wg = function (a) {
                h = a
            };
            V = new ed;
            V.M(o);
            Sb && V.M(n)
        }

        function Qc() {
            var c = this, a = Dc();
            b.N(a, 0);
            c.$Elmt = a;
            c.Ef = function (c) {
                b.O(a, c);
                b.mb(a)
            };
            c.Ob = function () {
                b.Fc(a);
                b.Rb(a)
            }
        }

        function bd(w, h) {
            var g = this, hb = b.W(g, p), z, H = 0, V, y, u, F, K, o, E = [], U, M, J, i, s, A, S;
            l.call(g, -N, N + 1, {hc: C & 1 ? q : f, $Reverse: Hb});

            function Q() {
                z && z.$Destroy();
                Xb -= H;
                H = 0;
                z = new kb.$Class(y, kb, {$Idle: b.q(y, "idle", Kb), cg: !t});
                z.$On(n.Zb, X)
            }

            function X(b, a) {
                H += a;
                Xb += a;
                if (h == r) !H && g.Bc()
            }

            function P(p, s, n) {
                if (!M) {
                    M = d;
                    if (o && n) {
                        var q = b.q(o, "data-expand", 0) * 2, f = n.width, e = n.height, l = f, i = e;
                        if (f && e) {
                            if (F) {
                                if (F & 3 && (!(F & 4) || f > I || e > G)) {
                                    var m = k, r = I / G * e / f;
                                    if (F & 1) m = r > 1; else if (F & 2) m = r < 1;
                                    l = m ? f * G / e : I;
                                    i = m ? G : e * I / f
                                }
                                b.K(o, l);
                                b.J(o, i);
                                b.V(o, (G - i) / 2);
                                b.U(o, (I - l) / 2)
                            }
                            b.we(o, c.l((l + q) / l, (i + q) / i))
                        }
                        b.db(o, "absolute")
                    }
                    a.k(j.$EVT_LOAD_END, h)
                }
                s.Qe(k);
                p && p(g)
            }

            function W(f, b, c, e) {
                if (e == A && r == h && t && Ib() && !g.Oc()) {
                    var a = v(f);
                    D.Cf(a, h, b, g, c, G / I);
                    rb.$Shift(a - rb.yc() - 1);
                    rb.L(a);
                    b.Tg();
                    pc(a, d)
                }
            }

            function Z(b) {
                if (b == A && r == h && Ib() && !g.Oc()) {
                    if (!i) {
                        var a = e;
                        if (D) if (D.Qb == h) a = D.of(); else D.Ob();
                        i = new ad(w, h, a, z);
                        i.zg(s)
                    }
                    !i.$IsPlaying() && i.sd()
                }
            }

            function L(a, d, k) {
                if (a == h) {
                    if (a != d) x[d] && x[d].Jd(); else !k && i && i.Ag();
                    s && s.$Enable();
                    A = b.Tb();
                    g.Vb(b.Z(e, Z, A))
                } else {
                    var j = c.j(h, a), f = c.l(h, a), n = c.j(f - j, j + q - f), l = N + m.$LazyLoading - 1;
                    (!J || n <= l) && g.Vb()
                }
            }

            function bb() {
                if (r == h && i) {
                    i.S();
                    s && s.$Quit();
                    s && s.$Disable();
                    i.he()
                }
            }

            function fb() {
                r == h && i && i.S()
            }

            function Y(b) {
                !db && a.k(j.$EVT_CLICK, h, b)
            }

            g.Qe = function (a) {
                if (S != a) {
                    S = a;
                    a && b.O(w, K);
                    !a && b.ib(K)
                }
            };
            g.Vb = function (f, c) {
                c = c || g;
                if (b.A(E) && !M) {
                    c.Qe(d);
                    if (!U) {
                        U = d;
                        a.k(j.$EVT_LOAD_START, h);
                        b.f(E, function (a) {
                            var c = b.g(a, "data-load") || "src", d = !b.Qd(c, "data-") ? c.substring(5) : c;
                            if (!b.g(a, d)) {
                                var e = b.hb(a, d) || b.hb(a, "src2");
                                if (e) {
                                    b.g(a, d, e);
                                    b.nb(a, b.g(a, "data-display"))
                                }
                            }
                        })
                    }
                    b.Eh(E, o, b.Z(e, P, f, c))
                } else P(f, c)
            };
            g.Gg = function () {
                if (Wc()) if (q == 1) {
                    g.Jd();
                    L(h, h)
                } else {
                    var a;
                    if (D) a = D.Bf(q);
                    if (a) {
                        A = b.Tb();
                        var c = h + eb, d = x[v(c)];
                        return d.Vb(b.Z(e, W, c, d, a, A), g)
                    } else (C || !sb(B.z()) || !sb(B.z() + eb)) && Wb(eb)
                }
            };
            g.Bc = function () {
                L(h, h, d)
            };
            g.Jd = function () {
                s && s.$Quit();
                s && s.$Disable();
                g.Wd();
                i && i.Hg();
                i = e;
                Q()
            };
            g.Tg = function () {
                b.Fc(w)
            };
            g.Wd = function () {
                b.mb(w)
            };

            function T(a, c) {
                if (!c) {
                    u = b.$FindChild(a, "bg");
                    y = u && b.Lb(u)
                }
                if (!b.g(a, Ob) && (c || !u)) {
                    var l = b.q(a, "data-arr");
                    if (l != f) {
                        function k(d, c) {
                            b.g(d, c, b.g(a, c))
                        }

                        var j = kb && kb.$Transitions || {};
                        b.Vf(a, b.cb(a), j[l], function (a, c) {
                            b.g(a, "data-t", b.A(j));
                            j.push(c);
                            k(a, "data-to");
                            k(a, "data-bf");
                            k(a, "data-c")
                        });
                        b.g(a, "data-arr", "")
                    }
                    var g = b.jb(a);
                    if (!u) {
                        y = a;
                        u = Dc(d);
                        b.g(u, "data-u", "bg");
                        var h = "background";
                        b.R(u, h + "Color", b.R(y, h + "Color"));
                        b.R(u, h + "Image", b.R(y, h + "Image"));
                        b.R(y, h, e);
                        b.A(g) ? b.pb(u, g[0]) : b.O(y, u)
                    }
                    g = g.concat(b.xc(b.Hc(a, "data-tchd")));
                    b.f(g, function (d) {
                        if (c < 3 && !o) if (b.hb(d, "u") == "image") {
                            o = d;
                            o.border = 0;
                            b.rb(o, ab);
                            b.rb(a, ab);
                            b.R(o, "maxWidth", "10000px");
                            b.O(u, o)
                        }
                        T(d, c + 1)
                    });
                    if (c) {
                        b.g(a, "data-events", b.lc(a));
                        b.g(a, "data-display", b.nb(a));
                        !b.Ib(a) && b.ug(a, b.g(a, "data-to"));
                        b.tg(a, b.g(a, "data-bf"));
                        if (a.tagName == "IMG") {
                            E.push(a);
                            if (!b.g(a, "src")) {
                                J = d;
                                b.Fc(a)
                            }
                        }
                        var i = b.g(a, "data-load");
                        i && E.push(a) && (J = J || !b.Qd(i, "data-"));
                        var m = i && b.g(a, i) || b.Jf(a);
                        if (m) {
                            var n = new Image;
                            b.g(n, "data-src", m);
                            E.push(n)
                        }
                        c && b.N(a, (b.N(a) || 0) + 1)
                    }
                    b.yg(a, b.q(a, "data-p"));
                    b.xg(a, b.hb(a, "po"));
                    b.Jc(a, b.g(a, "data-ts"))
                }
            }

            g.kd = function (c, b) {
                var a = N - b;
                Fc(V, a)
            };
            g.Qb = h;
            T(w, 0);
            b.rb(w, ab);
            b.Fb(w, "hidden");
            b.Jc(w, "flat");
            F = b.q(y, "data-fillmode", m.$FillMode);
            var O = b.$FindChild(y, "thumb", d);
            if (O) {
                g.nh = b.ab(O);
                b.Fc(O)
            }
            b.mb(w);
            K = b.ab(R);
            b.N(K, 1e3);
            g.a(w, "click", Y);
            Q();
            g.ih = o;
            g.Re = w;
            g.Wc = V = w;
            g.a(a, 203, L);
            g.a(a, 28, fb);
            g.a(a, 24, bb);
            g.$Destroy = function () {
                b.$Destroy(hb, z, i)
            }
        }

        function ad(F, h, q, s) {
            var c = this, E = b.W(c, p), i = 0, u = 0, g, m, f, e, o, w, v, z = x[h];
            l.call(c, 0, 0);

            function B() {
                c.sd()
            }

            function C(a) {
                v = a;
                c.S();
                c.sd()
            }

            function A() {
            }

            c.sd = function () {
                if (!y && !fb && !v && r == h && !c.Oc()) {
                    var k = c.z();
                    if (!k) if (g && !o) {
                        o = d;
                        c.he(d);
                        a.k(j.$EVT_SLIDESHOW_START, h, u, i, u, g, e)
                    }
                    a.k(j.$EVT_STATE_CHANGE, h, k, i, m, f, e);
                    if (!Jb()) {
                        var l;
                        if (k == e) t && b.$Delay(z.Gg, 20); else {
                            if (k == f) l = e; else if (!k) l = f; else l = c.Ee();
                            (k != f || !Ic()) && c.tc(l, B)
                        }
                    }
                }
            };
            c.Ag = function () {
                f == e && f == c.z() && c.L(m)
            };
            c.Hg = function () {
                D && D.Qb == h && D.Ob();
                var b = c.z();
                b < e && a.k(j.$EVT_STATE_CHANGE, h, -b - 1, i, m, f, e)
            };
            c.he = function (a) {
                q && b.Fb(T, a && q.ye.$Outside ? "" : "hidden")
            };
            c.kd = function (c, b) {
                if (o && b >= g) {
                    o = k;
                    z.Wd();
                    D.Ob();
                    a.k(j.$EVT_SLIDESHOW_END, h, g, i, u, g, e)
                }
                a.k(j.$EVT_PROGRESS_CHANGE, h, b, i, m, f, e)
            };
            c.zg = function (a) {
                if (a && !w) {
                    w = a;
                    a.$On($JssorPlayer$.vf, C)
                }
            };
            c.a(s, n.pc, A);
            q && c.zd(q);
            g = c.vb();
            c.zd(s);
            m = g + s.qc;
            e = c.vb();
            f = t ? g + s.fd : e;
            c.$Destroy = function () {
                E.$Destroy();
                c.S()
            }
        }

        function rc() {
            Nb = fb;
            hc = A.Ee();
            bb = B.z();
            hb = Nc(bb)
        }

        function Kc() {
            rc();
            if (y || Jb()) {
                A.S();
                a.k(j.kg)
            }
        }

        function Jc(f) {
            if (Ib()) {
                var b = B.z(), a = hb, e = 0;
                if (f && c.P(L) >= m.$MinDragOffsetToSlide) {
                    a = b;
                    e = Db
                }
                a = c.H(a);
                a = xb(a + e, .5);
                var d = c.P(a - b);
                if (d < 1 && m.$SlideEasing != g.$Linear) d = c.B(d, .5);
                if ((!db || !f) && Nb) A.tc(hc); else if (b == a) tc.Bc(); else A.se(b, a, d * Gb)
            }
        }

        function gc(a) {
            !b.kb(b.$EvtSrc(a), f, o.ze) && b.$CancelEvent(a)
        }

        function Ac(b) {
            Fb = k;
            y = d;
            Kc();
            if (!Nb) z = 0;
            a.k(j.$EVT_DRAG_START, v(bb), bb, b)
        }

        function Yc(a) {
            Ec(a, 1)
        }

        function Ec(c, d) {
            L = 0;
            Ab = 0;
            Db = 0;
            kc = sc;
            if (d) {
                var i = c.touches[0];
                Eb = {x: i.clientX, y: i.clientY}
            } else Eb = b.Tc(c);
            var e = b.$EvtSrc(c), g = b.kb(e, "1", ic);
            if ((!g || g === u) && !W && (!d || b.A(c.touches) == 1)) {
                nb = b.kb(e, f, o.ze) || !mb || !Zc();
                a.a(h, d ? "touchmove" : "mousemove", ac);
                Fb = !nb && b.kb(e, f, o.Dd);
                !Fb && !nb && Ac(c, d)
            }
        }

        function ac(a) {
            var e, f;
            a = b.Zf(a);
            if (a.type != "mousemove") if (b.A(a.touches) == 1) {
                f = a.touches[0];
                e = {x: f.clientX, y: f.clientY}
            } else gb(); else e = b.Tc(a);
            if (e) {
                var i = e.x - Eb.x, j = e.y - Eb.y, g = c.P(i), h = c.P(j);
                if (z || g > 1.5 || h > 1.5) if (Fb) Ac(a, f); else {
                    if (c.G(hb) != hb) z = z || S & W;
                    if ((i || j) && !z) {
                        if (W == 3) if (h > g) z = 2; else z = 1; else z = W;
                        if (Vb && z == 1 && h > g * 2.4) nb = d
                    }
                    var l = i, k = ob;
                    if (z == 2) {
                        l = j;
                        k = pb
                    }
                    (L - Ab) * qb < -1.5 && (Db = 0);
                    (L - Ab) * qb > 1.5 && (Db = -1);
                    Ab = L;
                    L = l;
                    mc = hb - L * qb / k / kc * m.$DragRatio;
                    if (L && z && !nb) {
                        b.$CancelEvent(a);
                        A.Ng(d);
                        A.Wg(mc)
                    }
                }
            }
        }

        function gb() {
            Uc();
            a.T(h, "mousemove", ac);
            a.T(h, "touchmove", ac);
            db = L;
            if (y) {
                db && t & 8 && (t = 0);
                A.S();
                y = k;
                var b = B.z();
                a.k(j.$EVT_DRAG_END, v(b), b, v(bb), bb);
                Y & 12 && rc();
                Jc(d)
            }
        }

        function Oc(c) {
            var e = b.$EvtSrc(c), a = b.kb(e, "1", Ob);
            if (u === a) if (db) {
                b.$StopEvent(c);
                a = b.kb(e, f, "data-jssor-button", "A");
                a && b.$CancelEvent(c)
            } else {
                t & 4 && (t = 0);
                a = b.kb(e, f, "data-jssor-click");
                if (a) {
                    b.$CancelEvent(c);
                    hitValues = (b.g(a, "data-jssor-click") || "").split(":");
                    var g = b.Fh(hitValues[1]);
                    hitValues[0] == "to" && tb(g - 1);
                    hitValues[0] == "next" && tb(g, f, d)
                }
            }
        }

        a.$SlidesCount = function () {
            return q
        };
        a.$CurrentIndex = function () {
            return r
        };
        a.$CurrentPosition = function () {
            return B.z()
        };
        a.$Idle = function (a) {
            if (a == f) return Kb;
            Kb = a
        };
        a.$AutoPlay = function (a) {
            if (a == f) return t;
            if (a != t) {
                t = a;
                t && x[r] && x[r].Bc()
            }
        };
        a.$IsDragging = function () {
            return y
        };
        a.$IsSliding = function () {
            return fb
        };
        a.$IsMouseOver = function () {
            return !U
        };
        a.$LastDragSucceeded = function () {
            return db
        };
        a.$OriginalWidth = function () {
            return O
        };
        a.$OriginalHeight = function () {
            return M
        };
        a.$ScaleHeight = function (b) {
            if (b == f) return Cc || M;
            a.$ScaleSize(b / M * O, b)
        };
        a.$ScaleWidth = function (b) {
            if (b == f) return Zb || O;
            a.$ScaleSize(b, b / O * M)
        };
        a.$ScaleSize = function (c, a, d) {
            b.K(u, c);
            b.J(u, a);
            Hc = c / O;
            Bc = a / M;
            b.f(nc, function (a) {
                a.$ScaleSize(Hc, Bc, d)
            });
            if (!Zb) {
                b.pb(T, w);
                b.V(T, 0);
                b.U(T, 0)
            }
            Zb = c;
            Cc = a
        };
        a.lf = yc;
        a.ef = wc;
        a.$PlayTo = tb;
        a.$GoTo = ub;
        a.$Next = function () {
            Wb(1)
        };
        a.$Prev = function () {
            Wb(-1)
        };
        a.$Pause = function () {
            t = 0
        };
        a.$Play = function () {
            a.$AutoPlay(t || 1)
        };
        a.$SetSlideshowTransitions = function (a) {
            m.$SlideshowOptions.$Transitions = a
        };
        a.Id = function (a) {
            a = v(a);
            if (C & 1) {
                var d = F / E, b = v(B.z()), e = v(a - b + d), f = v(c.P(a - b));
                if (e >= N) {
                    if (f > q / 2) if (a > b) a -= q; else a += q
                } else if (a > b && e < d) a -= q; else if (a < b && e > d) a += q
            }
            return a
        };

        function Xc() {
            cc.re && b.R(w, cc.re, ([e, "pan-y", "pan-x", "auto"])[mb] || "");
            a.a(u, "click", Oc, d);
            a.a(u, "mouseleave", Mc);
            a.a(u, "mouseenter", Lc);
            a.a(u, "mousedown", Ec);
            a.a(u, "touchstart", Yc);
            a.a(u, "dragstart", gc);
            a.a(u, "selectstart", gc);
            a.a(i, "mouseup", gb);
            a.a(h, "mouseup", gb);
            a.a(h, "touchend", gb);
            a.a(h, "touchcancel", gb);
            a.a(i, "blur", gb);
            m.$ArrowKeyNavigation && a.a(h, "keydown", function (c) {
                if (!b.qe(b.$EvtSrc(c))) {
                    var a = b.Je(c);
                    if (a == 37 || a == 39) {
                        t & 8 && (t = 0);
                        fc(m.$ArrowKeyNavigation * (a - 38) * qb, d)
                    }
                }
            })
        }

        function uc(d) {
            Gc.Ve();
            H = [];
            x = [];
            var e = b.jb(w), g = b.Fd(["DIV", "A", "LI"]);
            b.f(e, function (a) {
                var c = a;
                if (g[a.tagName.toUpperCase()] && !b.hb(a, "u") && b.nb(a) != "none") {
                    b.Jc(a, "flat");
                    b.rb(a, ab);
                    H.push(a)
                }
                b.N(c, (b.N(c) || 0) + 1)
            });
            q = b.A(H);
            if (q) {
                var a = S & 1 ? zb : yb;
                b.rb(R, ab);
                F = m.$Align;
                if (F == f) F = (a - E + P) / 2;
                lb = a / E;
                N = c.j(q, m.$Cols || q, c.H(lb));
                C = N < q ? m.$Loop : 0;
                if (q * E - P <= a) {
                    lb = q - P / E;
                    F = (a - E + P) / 2;
                    Lb = (a - E * q + P) / 2
                }
                if (Cb) {
                    Qb = Cb.$Class;
                    Sb = !F && N == 1 && q > 1 && Qb && (!b.ue() || b.Cd() >= 9)
                }
                if (!(C & 1)) {
                    cb = F / E;
                    if (cb > q - 1) {
                        cb = q - 1;
                        F = cb * E
                    }
                    K = cb;
                    Q = K + q - lb - P / E
                }
                mb = (N > 1 || F ? S : -1) & m.$DragOrientation;
                if (Sb) D = new Qb(Bb, I, G, Cb, Vb, lc);
                b.f(H, function (a, b) {
                    x.push(new bd(a, b))
                });
                rb = new cd;
                B = new dd;
                A = new Tc(B, rb);
                Xc()
            }
            b.f(Z, function (a) {
                a.nd(q, x);
                d && a.$On(s.uc, fc)
            })
        }

        function Pb(a, d, g) {
            b.Md(a) && (a = b.je("", a));
            var c, e;
            if (q) {
                if (d == f) d = q;
                e = "beforebegin";
                c = H[d];
                if (!c) {
                    e = "afterend";
                    c = H[q - 1]
                }
            }
            b.$Destroy(x);
            a && b.oh(c || w, e || "afterbegin", a);
            b.f(g, function (a) {
                b.ib(a)
            });
            uc()
        }

        a.$AppendSlides = function (e, a) {
            if (a == f) a = r + 1;
            var d = H[r];
            Pb(e, a);
            var c = 0;
            b.f(H, function (a, b) {
                a == d && (c = b)
            });
            ub(c)
        };
        a.$ReloadSlides = function (a) {
            Pb(a, e, H);
            ub(0)
        };
        a.$RemoveSlides = function (f) {
            var a = r, d = [];
            b.f(f, function (b) {
                if (b < q && b >= 0) {
                    d.push(H[b]);
                    b < r && a--
                }
            });
            Pb(e, e, d);
            a = c.j(a, q - 1);
            ub(a)
        };
        a.F = function (i, e) {
            a.$Elmt = u = b.$GetElement(i);
            O = b.K(u);
            M = b.J(u);
            m = b.v({
                $FillMode: 0,
                $LazyLoading: 1,
                $ArrowKeyNavigation: 1,
                $StartIndex: 0,
                $AutoPlay: 0,
                $Loop: 1,
                $HWA: d,
                $NaviQuitDrag: d,
                $AutoPlaySteps: 1,
                $Idle: 3e3,
                $PauseOnHover: 1,
                $SlideDuration: 500,
                $SlideEasing: g.$OutQuad,
                $MinDragOffsetToSlide: 20,
                $DragRatio: 1,
                $SlideSpacing: 0,
                $UISearchMode: 1,
                $PlayOrientation: 1,
                $DragOrientation: 1
            }, e);
            m.$HWA = m.$HWA && b.gg();
            if (m.$DisplayPieces != f) m.$Cols = m.$DisplayPieces;
            if (m.$ParkingPosition != f) m.$Align = m.$ParkingPosition;
            t = m.$AutoPlay & 63;
            !m.$UISearchMode;
            eb = m.$AutoPlaySteps;
            Y = m.$PauseOnHover;
            Y &= Vb ? 10 : 5;
            Kb = m.$Idle;
            Gb = m.$SlideDuration;
            S = m.$PlayOrientation & 3;
            vb = b.mg(b.g(u, "dir")) == "rtl";
            Hb = vb && (S == 1 || m.$DragOrientation & 1);
            qb = Hb ? -1 : 1;
            Cb = m.$SlideshowOptions;
            kb = b.v({$Class: n}, m.$CaptionSliderOptions);
            jb = m.$BulletNavigatorOptions;
            X = m.$ArrowNavigatorOptions;
            J = m.$ThumbnailNavigatorOptions;
            var c = b.jb(u);
            b.f(c, function (a, d) {
                var c = b.hb(a, "u");
                if (c == "loading") R = a; else {
                    if (c == "slides") {
                        w = a;
                        b.R(w, "margin", 0);
                        b.R(w, "padding", 0);
                        b.Jc(w, "flat")
                    }
                    if (c == "navigator") Mb = a;
                    if (c == "arrowleft") bc = a;
                    if (c == "arrowright") Yb = a;
                    if (c == "thumbnavigator") wb = a;
                    if (a.tagName != "STYLE" && a.tagName != "SCRIPT") nc[c || d] = new Rc(a, c == "slides", b.Fd(["slides", "thumbnavigator"])[c])
                }
            });
            R && b.ib(R);
            R = R || b.bc(h);
            zb = b.K(w);
            yb = b.J(w);
            I = m.$SlideWidth || zb;
            G = m.$SlideHeight || yb;
            ab = {Eb: I, Gb: G, $Top: 0, $Left: 0, Me: "block", Pb: "absolute"};
            P = m.$SlideSpacing;
            ob = I + P;
            pb = G + P;
            E = S & 1 ? ob : pb;
            Bb = new Qc;
            b.g(u, Ob, "1");
            b.N(w, b.N(w) || 0);
            b.db(w, "absolute");
            T = b.ab(w, d);
            b.R(T, "pointerEvents", "none");
            b.pb(T, w);
            b.O(T, Bb.$Elmt);
            b.Fb(w, "hidden");
            if (Mb && jb) {
                jb.Yb = vb;
                vc = new jb.$Class(Mb, jb, O, M);
                Z.push(vc)
            }
            if (X && bc && Yb) {
                X.Yb = vb;
                X.$Loop = m.$Loop;
                xc = new X.$Class(bc, Yb, X, a);
                Z.push(xc)
            }
            if (wb && J) {
                J.$StartIndex = m.$StartIndex;
                J.$ArrowKeyNavigation = J.$ArrowKeyNavigation || 0;
                J.Yb = vb;
                oc = new J.$Class(wb, J, R);
                !J.$NoDrag && b.g(wb, ic, "1");
                Z.push(oc)
            }
            uc(d);
            a.$ScaleSize(O, M);
            Ub();
            ub(m.$StartIndex);
            b.R(u, "visibility", "visible")
        };
        a.$Destroy = function () {
            t = 0;
            b.$Destroy(x, Z, Gc);
            b.Rb(u)
        };
        b.F(a)
    };
    j.$EVT_CLICK = 21;
    j.$EVT_DRAG_START = 22;
    j.$EVT_DRAG_END = 23;
    j.$EVT_SWIPE_START = 24;
    j.$EVT_SWIPE_END = 25;
    j.$EVT_LOAD_START = 26;
    j.$EVT_LOAD_END = 27;
    j.kg = 28;
    j.$EVT_MOUSE_ENTER = 31;
    j.$EVT_MOUSE_LEAVE = 32;
    j.$EVT_POSITION_CHANGE = 202;
    j.$EVT_PARK = 203;
    j.$EVT_SLIDESHOW_START = 206;
    j.$EVT_SLIDESHOW_END = 207;
    j.$EVT_PROGRESS_CHANGE = 208;
    j.$EVT_STATE_CHANGE = 209
}(window, document, Math, null, true, false)