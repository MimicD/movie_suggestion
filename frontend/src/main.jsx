import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import * as Pages from './pages/index.js';


import { createBrowserRouter, RouterProvider } from 'react-router-dom'

const router = createBrowserRouter([
  //Public routes
  {path: "/", element: <Pages.MainPage />}, //Main app page
  {path: "/login", element: <Pages.LoginPage />}, //Login page
  {path: "/register", element: <Pages.RegisterPage />}, //Register page
  
  //Authorized routs

  {path: "*", element: <Pages.NotFoundPage />}, //Redirect to 404 page
])

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
