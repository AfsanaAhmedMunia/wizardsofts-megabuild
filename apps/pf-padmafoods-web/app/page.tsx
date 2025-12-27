'use client';

import type { Metadata } from "next";
import { useEffect } from "react";

// Google Analytics Script
function GoogleAnalytics() {
  useEffect(() => {
    const gaId = process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID;
    if (!gaId) return;

    // Load Google Analytics script
    const script1 = document.createElement('script');
    script1.async = true;
    script1.src = `https://www.googletagmanager.com/gtag/js?id=${gaId}`;
    document.head.appendChild(script1);

    // Initialize gtag
    const script2 = document.createElement('script');
    script2.innerHTML = `
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', '${gaId}');
    `;
    document.head.appendChild(script2);
  }, []);

  return null;
}

export default function ComingSoonPage() {
  return (
    <>
      <GoogleAnalytics />
      <div className="min-h-screen bg-red-600 flex items-center justify-center px-4 py-8">
        <div className="text-center max-w-2xl mx-auto w-full">
          {/* Logo */}
          <div className="mb-8 md:mb-12">
            {/* Circular Logo - Red background with orange circle */}
            <div className="mx-auto mb-6 w-32 h-32 md:w-40 md:h-40 bg-orange-500 rounded-full flex items-center justify-center shadow-2xl relative">
              {/* Curved accent */}
              <div className="absolute inset-0 rounded-full border-4 border-blue-300/30"></div>
              {/* Spoon icon */}
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-16 w-16 md:h-20 md:w-20 text-white"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={1.5}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M12 6v12m6-6H6"
                />
              </svg>
            </div>

            {/* Brand Name */}
            <h1 className="text-3xl md:text-5xl font-bold text-white mb-2">
              Padma Foods
            </h1>
            <p className="text-lg md:text-xl text-orange-100 font-medium">
              Quality Assured • Authentic Taste
            </p>
          </div>

          {/* Main Message */}
          <div className="mb-10 md:mb-14">
            <h2 className="text-2xl md:text-3xl font-bold text-white mb-4">
              Coming Soon
            </h2>
            <p className="text-base md:text-lg text-orange-50 leading-relaxed">
              Fresh, authentic Bangladeshi food products delivered to your door.
              Stay tuned for our official launch!
            </p>
          </div>

          {/* Contact Section */}
          <div className="bg-white/15 backdrop-blur-sm rounded-2xl p-6 md:p-8 border border-white/20 mb-8">
            <p className="text-white font-semibold mb-6 text-sm md:text-base">
              Get in touch with us:
            </p>

            {/* Contact Grid */}
            <div className="space-y-4">
              {/* Phone Numbers */}
              <div className="flex items-center justify-center gap-2 flex-wrap">
                <a
                  href="tel:+8801713492481"
                  className="inline-flex items-center gap-2 px-4 py-2 bg-white text-red-600 rounded-lg font-semibold hover:bg-orange-50 transition-colors text-sm md:text-base"
                >
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.893.953a15.13 15.13 0 006.917 6.917l.953-1.893a1 1 0 011.06-.54l4.435.74a1 1 0 01.836.986V17a2 2 0 01-2 2h-2.5a7.5 7.5 0 01-7.5-7.5V5a2 2 0 01-2-2z" />
                  </svg>
                  +880 1713-492481
                </a>
                <a
                  href="tel:+8801713492482"
                  className="inline-flex items-center gap-2 px-4 py-2 bg-white text-red-600 rounded-lg font-semibold hover:bg-orange-50 transition-colors text-sm md:text-base"
                >
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.893.953a15.13 15.13 0 006.917 6.917l.953-1.893a1 1 0 011.06-.54l4.435.74a1 1 0 01.836.986V17a2 2 0 01-2 2h-2.5a7.5 7.5 0 01-7.5-7.5V5a2 2 0 01-2-2z" />
                  </svg>
                  +880 1713-492482
                </a>
              </div>

              {/* Social Links */}
              <div className="flex items-center justify-center gap-3">
                <a
                  href="https://www.facebook.com/padmafoods"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center justify-center w-10 h-10 bg-white text-blue-600 rounded-full hover:bg-orange-50 transition-colors"
                  title="Visit our Facebook page"
                >
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
                  </svg>
                </a>
              </div>
            </div>
          </div>

          {/* Footer */}
          <p className="text-white/70 text-xs md:text-sm">
            &copy; {new Date().getFullYear()} Padma Foods. All rights reserved.
          </p>
        </div>
      </div>
    </>
  );
}
