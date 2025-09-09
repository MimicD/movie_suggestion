import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import * as Pages from './pages/index.js';

import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { AuthProvider } from './components/AuthContext.jsx';
//import { PrivateRoute } from './components/PrivateRoute.jsx';

const router = createBrowserRouter([
  // Public routes
  { path: "/", element: <Pages.MainPage /> },
  { path: "/login", element: <Pages.LoginPage /> },
  { path: "/register", element: <Pages.RegisterPage /> },

  // Protected route
  // {
  //   path: "/profile",
  //   element: (
  //     <PrivateRoute>
  //       <Pages.ProfilePage />
  //     </PrivateRoute>
  //   )
  // },

  { path: "*", element: <Pages.NotFoundPage /> },
])

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  </StrictMode>,
)
