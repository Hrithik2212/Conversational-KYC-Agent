import React from 'react'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from './pages/home/Home'
import KYC from './pages/kyc/KYC';
const App = () => {

  
  return (
    <div>
      <BrowserRouter>
        <Routes>
              <Route path='/' index element={<Home />} />
              <Route path="/apply" element={<KYC />} />
              
              
        </Routes>
    </BrowserRouter>

    </div>
  )
}

export default App