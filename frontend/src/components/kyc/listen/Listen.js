import React from 'react'
import './ListeningAnimation.css';
const Listen = () => {
  return (
    <div className="w-full h-full text-center leading-[8rem]">
        <svg viewBox="0 0 100 100" className='listening-animation'>
            <circle cx="50" cy="50" r="40" fill='none'  stroke="rgb(59 130 246)" strokeWidth="4" />
      
            <rect x="20" y="30" width="10" height="40" fill="rgb(59 130 246)" />
            <rect x="35" y="30" width="10" height="20" fill="rgb(59 130 246)" />
            <rect x="50" y="30" width="10" height="35" fill="rgb(59 130 246)" /> 
            <rect x="65" y="30" width="10" height="25" fill="rgb(59 130 246)" /> 
      </svg>
      <p className='text-[36px] font-[600]'>Listen...</p>
    </div>
  )
}

export default Listen