'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import * as DropdownMenu from '@radix-ui/react-dropdown-menu';
import * as Dialog from '@radix-ui/react-dialog';
import { 
  LayoutDashboard, 
  BarChart3, 
  Users, 
  Settings, 
  Bell,
  Search,
  Menu,
  X,
  User,
  LogOut,
  HelpCircle,
} from 'lucide-react';

export default function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const pathname = usePathname();

  const navItems = [
    { href: '/', label: 'Dashboard', icon: LayoutDashboard },
    { href: '/analytics', label: 'Analytics', icon: BarChart3 },
    { href: '/users', label: 'Users', icon: Users },
    { href: '/settings', label: 'Settings', icon: Settings },
  ];

  const isActive = (href: string) => {
    if (href === '/') {
      return pathname === '/';
    }
    return pathname.startsWith(href);
  };

  return (
    <nav className="fixed top-0 w-full bg-slate-900 border-b border-slate-800 z-50">
      <div className="px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo and Desktop Nav */}
          <div className="flex items-center space-x-8">
            <Link href="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <LayoutDashboard className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold">Dashboard</span>
            </Link>

            {/* Desktop Navigation Links */}
            <div className="hidden md:flex space-x-1">
              {navItems.map((item) => {
                const Icon = item.icon;
                const active = isActive(item.href);
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    onClick={() => setMobileMenuOpen(false)}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                      active
                        ? 'bg-slate-800 text-white'
                        : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span>{item.label}</span>
                  </Link>
                );
              })}
            </div>
          </div>

          {/* Right Side Actions */}
          <div className="flex items-center space-x-4">
            {/* Search Button */}
            <button className="hidden sm:flex p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-colors">
              <Search className="w-5 h-5" />
            </button>

            {/* Notifications Dropdown
            <DropdownMenu.Root open={notificationsOpen} onOpenChange={setNotificationsOpen}>
              <DropdownMenu.Trigger asChild>
                <button className="p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-colors relative">
                  <Bell className="w-5 h-5" />
                  <span className="absolute top-1 right-1 w-2 h-2 bg-blue-500 rounded-full"></span>
                </button>
              </DropdownMenu.Trigger>

              <DropdownMenu.Portal>
                <DropdownMenu.Content
                  className="min-w-[320px] bg-slate-900 border border-slate-800 rounded-lg shadow-xl p-2 z-50"
                  sideOffset={8}
                  align="end"
                >
                  <div className="px-3 py-2 border-b border-slate-800 mb-2">
                    <h3 className="font-semibold text-white">Notifications</h3>
                  </div>
                  
                  {[1, 2, 3].map((i) => (
                    <DropdownMenu.Item
                      key={i}
                      className="px-3 py-3 rounded-md hover:bg-slate-800 cursor-pointer outline-none"
                    >
                      <p className="text-sm text-white">New user registration</p>
                      <p className="text-xs text-slate-400 mt-1">{i} minutes ago</p>
                    </DropdownMenu.Item>
                  ))}
                  
                  <DropdownMenu.Separator className="h-px bg-slate-800 my-2" />
                  
                  <DropdownMenu.Item className="px-3 py-2 text-sm text-blue-400 hover:bg-slate-800 rounded-md cursor-pointer outline-none text-center">
                    View all notifications
                  </DropdownMenu.Item>
                </DropdownMenu.Content>
              </DropdownMenu.Portal>
            </DropdownMenu.Root> */}

            {/* User Menu Dropdown */}
            <div className="hidden sm:flex items-center space-x-3 pl-4 border-l border-slate-800">
              <DropdownMenu.Root>
                <DropdownMenu.Trigger asChild>
                  <button className="w-8 h-8 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center text-sm font-semibold hover:ring-2 hover:ring-purple-400 transition-all">
                    JD
                  </button>
                </DropdownMenu.Trigger>

                <DropdownMenu.Portal>
                  <DropdownMenu.Content
                    className="min-w-[200px] bg-slate-900 border border-slate-800 rounded-lg shadow-xl p-2 z-50"
                    sideOffset={8}
                    align="end"
                  >
                    <div className="px-3 py-2 border-b border-slate-800 mb-2">
                      <p className="font-semibold text-white">John Doe</p>
                      <p className="text-xs text-slate-400">john@example.com</p>
                    </div>
                    
                    <DropdownMenu.Item className="flex items-center space-x-2 px-3 py-2 rounded-md hover:bg-slate-800 cursor-pointer outline-none">
                      <User className="w-4 h-4" />
                      <span className="text-sm">Profile</span>
                    </DropdownMenu.Item>
                    
                    <DropdownMenu.Item className="flex items-center space-x-2 px-3 py-2 rounded-md hover:bg-slate-800 cursor-pointer outline-none">
                      <Settings className="w-4 h-4" />
                      <span className="text-sm">Settings</span>
                    </DropdownMenu.Item>
                    
                    <DropdownMenu.Item className="flex items-center space-x-2 px-3 py-2 rounded-md hover:bg-slate-800 cursor-pointer outline-none">
                      <HelpCircle className="w-4 h-4" />
                      <span className="text-sm">Help</span>
                    </DropdownMenu.Item>
                    
                    <DropdownMenu.Separator className="h-px bg-slate-800 my-2" />
                    
                    <DropdownMenu.Item className="flex items-center space-x-2 px-3 py-2 rounded-md hover:bg-red-500/10 text-red-400 cursor-pointer outline-none">
                      <LogOut className="w-4 h-4" />
                      <span className="text-sm">Log out</span>
                    </DropdownMenu.Item>
                  </DropdownMenu.Content>
                </DropdownMenu.Portal>
              </DropdownMenu.Root>
            </div>

            {/* Mobile menu button */}
            <Dialog.Root open={mobileMenuOpen} onOpenChange={setMobileMenuOpen}>
              <Dialog.Trigger asChild>
                <button className="md:hidden p-2 rounded-lg hover:bg-slate-800 transition-colors">
                  <Menu className="w-6 h-6" />
                </button>
              </Dialog.Trigger>

              <Dialog.Portal>
                <Dialog.Overlay className="fixed inset-0 bg-black/50 z-40" />
                <Dialog.Content className="fixed top-0 right-0 h-full w-64 bg-slate-900 border-l border-slate-800 z-50 p-6">
                  <div className="flex items-center justify-between mb-6">
                    <Dialog.Title className="text-lg font-bold">Menu</Dialog.Title>
                    <Dialog.Close asChild>
                      <button className="p-2 rounded-lg hover:bg-slate-800 transition-colors">
                        <X className="w-5 h-5" />
                      </button>
                    </Dialog.Close>
                  </div>

                  <div className="space-y-1">
                    {navItems.map((item) => {
                      const Icon = item.icon;
                      const active = isActive(item.href);
                      return (
                        <Link
                          key={item.href}
                          href={item.href}
                          onClick={() => setMobileMenuOpen(false)}
                          className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                            active
                              ? 'bg-slate-800 text-white'
                              : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
                          }`}
                        >
                          <Icon className="w-5 h-5" />
                          <span>{item.label}</span>
                        </Link>
                      );
                    })}
                  </div>
                </Dialog.Content>
              </Dialog.Portal>
            </Dialog.Root>
          </div>
        </div>
      </div>
    </nav>
  );
}



// // components/TopBar.tsx
// "use client";
// import { usePathname } from 'next/navigation';
// import Link from 'next/link';

// const navItems = [
//   { href: '/dashboard', label: 'Home' },
//   { href: '/analytics', label: 'Analytics' },
// ];


// export default function TopBar() {
//     const pathname = usePathname();

//     return (
//         {navItems.map((item: any) => (
//             <Link
//                 key={item.href}
//                 href={item.href}
//                 className={`px-3 py-2 text-sm font-medium rounded-md ${
//                 pathname === item.href
//                     ? 'bg-gray-900 text-white'
//                     : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
//                 }`}
//             >
//                 {item.label}
//             </Link>
//             ))}
//         // <nav className="bg-white border-b border-gray-200 fixed w-full z-30 top-0">
//         //     <div className="px-4 sm:px-6 lg:px-8">
//         //     <div className="flex justify-between h-16">
//         //         {/* Logo/Brand */}
//         //         <div className="flex items-center">
//         //         <Link href="/" className="flex items-center">
//         //             <span className="text-xl font-bold text-gray-900">Dashboard</span>
//         //         </Link>
//         //         </div>

//         //         {/* Navigation Links */}
//         //         <div className="hidden md:flex md:items-center md:space-x-8">
//         //         <Link href="/dashboard" className="text-gray-700 hover:text-gray-900 px-3 py-2 text-sm font-medium">
//         //             Home
//         //         </Link>
//         //         <Link href="/analytics" className="text-gray-700 hover:text-gray-900 px-3 py-2 text-sm font-medium">
//         //             Analytics
//         //         </Link>
//         //         <Link href="/users" className="text-gray-700 hover:text-gray-900 px-3 py-2 text-sm font-medium">
//         //             Users
//         //         </Link>
//         //         <Link href="/settings" className="text-gray-700 hover:text-gray-900 px-3 py-2 text-sm font-medium">
//         //             Settings
//         //         </Link>
//         //         </div>

//         //         {/* User Menu */}
//         //         <div className="flex items-center">
//         //         <button className="bg-gray-800 text-white rounded-full h-8 w-8 flex items-center justify-center">
//         //             U
//         //         </button>
//         //         </div>
//         //     </div>
//         //     </div>
//         // </nav>
//     );
// }