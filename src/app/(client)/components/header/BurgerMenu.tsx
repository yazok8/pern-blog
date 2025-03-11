import React, { useRef, useEffect } from 'react';
import Link from 'next/link';

interface BurgerMenuProps {
  isOpen: boolean;
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
}

function BurgerMenu({ isOpen, setIsOpen }: BurgerMenuProps) {
  const mobileMenuRef = useRef<HTMLDivElement>(null);


  // Handle clicks outside the mobile menu
  useEffect(() => {
    if (!isOpen) return;

    const handleClickOutsideMobileMenu = (event: MouseEvent) => {
      const target = event.target as Node;
      if (mobileMenuRef.current && !mobileMenuRef.current.contains(target)) {
        setIsOpen(false);
      }
    };

    // Prevent scrolling on body when menu is open
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    }

    document.addEventListener('mousedown', handleClickOutsideMobileMenu);

    return () => {
      document.removeEventListener('mousedown', handleClickOutsideMobileMenu);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, setIsOpen]);

  return (
    <div
      ref={mobileMenuRef}
      className={`fixed top-0 left-0 w-[50%] sm:w-[60%] h-screen bg-[#ecf0f3] sm:px-10 
                 ease-in-out duration-300 z-50 text-black transform mt-[80px] ${
                   isOpen ? 'translate-x-0' : '-translate-x-full'
                 } overflow-y-auto`}
    >
      <div className="flex justify-center items-center flex-col py-4">
      {/* <div className="cursor-pointer" onClick={toggleMenu}>
          <BsX className="h-8 w-8 text-black hover:text-[#f68519] transition-colors" />
        </div> */}
        <ul className="space-y-2 whitespace-nowrap">
          <li
            className="py-3 text-lg font-medium hover:text-[#f68519] transition-colors"
            onClick={() => setIsOpen(false)}
          >
            <Link href="/#about">Articles</Link>
          </li>
          <li
            className="py-3 text-lg font-medium hover:text-[#f68519] transition-colors"
            onClick={() => setIsOpen(false)}
          >
            <Link href="/#team">My story</Link>
          </li>
          <li
            className="py-3 text-lg font-medium hover:text-[#f68519] transition-colors"
            onClick={() => setIsOpen(false)}
          >
            <Link href="/#services">Post</Link>
          </li>
          <li
            className="py-3 text-lg font-medium hover:text-[#f68519] transition-colors"
            onClick={() => setIsOpen(false)}
          >
            <Link href="/#faq">FAQ</Link>
          </li>
          <li
            className="py-3 text-lg font-medium hover:text-[#f68519] transition-colors"
            onClick={() => setIsOpen(false)}
          >
            <Link href="/#contact">Join</Link>
          </li>
        </ul>
      </div>
    </div>
  );
}

export default BurgerMenu;