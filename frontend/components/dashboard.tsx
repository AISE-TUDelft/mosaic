// "use client";
// import React, { useState } from "react";
// import Link from "next/link";
// import TopBar from "./topBar";
// import { useRouter } from "next/navigation";

// export default function Dashboard({ children }: { children: React.ReactNode }) {
//   const router = useRouter();
//   // const [menuOpen, setMenuOpen] = useState(false);

//   const goToAboutUs = async () => {
//     await router.push("/about-us");
//   };

//   return (
//     <>
//       {/* <header className="bg-white dark:bg-gray-900 shadow">
//         <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
//           <div className="flex justify-between h-16 items-center">
//             <div className="flex items-center">
//               <Link href="/" className="text-xl font-semibold text-gray-900 dark:text-white">AISE</Link>
//               <nav className="hidden md:flex space-x-6 ml-6">
//                 <Link href="/reports" className="text-gray-700 dark:text-gray-200 hover:underline">Reports</Link>
//                 <Link href="/about-us" className="text-gray-700 dark:text-gray-200 hover:underline">About</Link>
//               </nav>
//             </div>

//             <div className="flex items-center">
//               <div className="hidden md:block">
//                 <button onClick={goToAboutUs} className="ml-4 bg-blue-600 text-white px-3 py-1 rounded-md">About Us</button>
//               </div>

//               <button
//                 aria-label="Toggle menu"
//                 onClick={() => setMenuOpen((s) => !s)}
//                 className="md:hidden inline-flex items-center justify-center p-2 rounded-md text-gray-700 dark:text-gray-200"
//               >
//                 {menuOpen ? (
//                   <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
//                     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
//                   </svg>
//                 ) : (
//                   <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
//                     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
//                   </svg>
//                 )}
//               </button>
//             </div>
//           </div>
//         </div>

//         {menuOpen && (
//           <div className="md:hidden bg-white dark:bg-gray-900 px-2 pt-2 pb-3 space-y-1">
//             <Link href="/reports" className="block px-3 py-2 rounded-md text-base font-medium">Reports</Link>
//             <Link href="/about-us" className="block px-3 py-2 rounded-md text-base font-medium">About</Link>
//           </div>
//         )}
//       </header>

//       <main className="p-6">
//         <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
//         <p className="mb-4">Welcome to the AISE dashboard. Use the navigation above to move between pages.</p>
//         <button onClick={goToAboutUs} className="bg-blue-600 text-white px-4 py-2 rounded">About Us</button>
//       </main> */}

//       <div className="min-h-screen bg-gray-50">
//         <TopBar />
//         <main className="pt-16"> {/* pt-16 offsets the fixed navbar */}
//           <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
//             {/* {children} */}
//             Dashboard

//           </div>
//         </main>
//       </div>
//     </>
//   );
// }
