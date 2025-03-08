import React from 'react'

interface AdminLayout {
    children:React.ReactNode
};

export default function AdminLayout({children}:AdminLayout) {
  return (
    <main className='p-4 pt-16 lg:pl-[250px] transition-all duration-300 min-h-screen'>{children}</main>
  )
}
