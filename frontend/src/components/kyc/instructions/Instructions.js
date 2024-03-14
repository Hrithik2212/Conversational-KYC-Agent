import React, { useState } from 'react'

const Instructions = () => {
    const [instructions,setInstructions]=useState(["Read the provided information carefully.","Double-check your Details before proceeding.","Please spell words properly.","Please speak when you observe the listening animation.","Please verify before clicking the next button.","Click the 'Next' button to continue."])
    const [show,setShow]=useState(true)
  return (
    (show ? (
        <div className='fixed top-[30%] left-[30%] z-[100]'>
          <div>
                <div className="max-w-xl mx-auto p-6 bg-white rounded shadow-md">
                        <h1 className="text-2xl font-bold mb-4">Instructions</h1>
                        <p className="text-gray-700 mb-4">
                          Welcome! To Online KYC Application:
                        </p>
                        <ol className="list-decimal pl-4 mb-4">
                        
                            {instructions.map((item,key)=>(
                              <li className='mb-2' key={key}>{item}</li>
                            ))}
                      
          
                        </ol>
                        <div className="mt-4">
                          <button onClick={()=>{setShow(false)}} className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700">Next</button>
                        </div>
                      </div>
          </div>
      </div>
    ):(
        null
    ))
  )
}

export default Instructions