"use client";

import React, { useRef, useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { BsList, BsX } from 'react-icons/bs';
import BurgerMenu from './BurgerMenu';


export default function Header() {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  
  const toggleMenu = () => setIsOpen(prev => !prev);
  const desktopServicesRef = useRef<HTMLDivElement>(null);

  // Handle scroll effect for navbar
  useEffect(() => {
    const handleScroll = () => {
      const scrollPosition = window.scrollY;
      if (scrollPosition > 10) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <>
      <nav 
        className={`w-full fixed h-16 sm:h-20 shadow-xl bg-blue-300 text-black z-50 transition-all duration-300 ${
          scrolled ? 'bg-opacity-95' : 'bg-opacity-100'
        }`}
      >
        <div className="px-4 sm:px-6 md:px-10 flex justify-end h-full max-w-7xl mx-auto items-center">
          {/* <Link href="/#">
            <Image
              src={khlogo}
              alt="kh consultation logo"
              width={100}
              height={100}
              className="cursor-pointer w-auto h-10 sm:h-12"
              priority
            />
          </Link>
           */}
          {/* Desktop Navigation */}
          <div className=" hidden md:flex text-sm lg:text-base xl:text-lg items-center space-x-1 lg:space-x-3 ml-auto">
          <Link 
              className="px-2 lg:px-4 py-2 whitespace-nowrap hover:text-[#f68519] transition-colors" 
              href="/home"
            >
              
            </Link>
            <Link 
              className="px-2 lg:px-4 py-2 whitespace-nowrap hover:text-[#f68519] transition-colors" 
              href="/articles"
            >
              Articles
            </Link>
            <Link 
              className="px-2 lg:px-4 py-2 whitespace-nowrap hover:text-[#f68519] transition-colors" 
              href="/my-story"
            >
              My story
            </Link>
            
            {/* Desktop Services Menu */}
            <div className="relative" ref={desktopServicesRef}>
              <Link 
                className="px-2 lg:px-4 py-2 whitespace-nowrap hover:text-[#f68519] transition-colors" 
                href="/post"
              >
                Post
              </Link>
            </div>
            <div className="relative" ref={desktopServicesRef}>
              <Link 
                className="px-2 lg:px-4 py-2 whitespace-nowrap hover:text-[#f68519] transition-colors" 
                href="/community"
              >
                Community
              </Link>
            </div>
            
            <Link 
              className="px-2 lg:px-4 py-2 whitespace-nowrap hover:text-[#f68519] transition-colors" 
              href="/#faq"
            >
              FAQ
            </Link>
            <Link 
              className="px-2 lg:px-4 py-2 whitespace-nowrap hover:text-[#f68519] transition-colors" 
              href="/join"
            >
              Join
            </Link>
            
          </div>
          
          {/* Mobile Menu Toggle */}
          <div className="flex items-center space-x-4">
            <div
              className="md:hidden cursor-pointer text-white ml-auto"
              onClick={toggleMenu}
              aria-label="Toggle menu"
            >
              {isOpen ? (
                <BsX className="h-8 w-8 hover:text-[#f68519] transition-colors" />
              ) : (
                <BsList className="h-8 w-8 hover:text-[#f68519] transition-colors" />
              )}
            </div>
          </div>
        </div>
        
        {/* Mobile Menu */}
        <BurgerMenu isOpen={isOpen} setIsOpen={setIsOpen} />

      </nav>
      {/* Spacer to prevent content from being hidden under fixed navbar */}
      <div className="h-16 sm:h-20"></div>
    </>
  );
}