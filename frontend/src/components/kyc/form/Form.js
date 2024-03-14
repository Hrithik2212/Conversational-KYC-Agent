import React, { useState } from 'react';
import Loading from '../../loading/Loading';
const FormComponent = ({data,setData}) => {



  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [show,setShow]=useState(true)

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        const data = await response.json();
        setMessage(data.message);
      } else {
        const errorData = await response.json();
        setMessage(`Error: ${errorData.message}`);
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      setMessage('Error uploading file. Please try again later.');
    }
  };


  // Function to handle form input changes
  const handleChange = (key, value) => {
    setData(prevState => ({
      ...prevState,
      [key]: value
    }));
  };

  // Function to handle form submission
  const handleSubmit = (event) => {
    event.preventDefault();
    console.log('Form submitted:', data);
  };

  return (
    <div>
      {show ? <Loading/>:(
        <form>
        {/* Iterate over formData and render form fields */}
        {Object.entries(data).map(([key, value]) => (
          <div key={key}>
            <label className='block mb-2 text-sm font-medium text-gray-900' htmlFor={key}>{key}</label>
            <input
              type="text"
              className='bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'
              id={key}
              name={key}
              value={value}
              onChange={(e) => handleChange(key, e.target.value)}
            />
            
          </div>
        ))}
        <div className='flex flex-col gap-3 mt-5'>
            <input type="file" onChange={handleFileChange} />
            <input type="file" onChange={handleFileChange} />
            <button className='bg-blue-500 text-white w-[50%] mx-auto' onClick={handleUpload}>Upload</button>
        </div>
        <button onClick={handleSubmit} className='bg-blue-500 w-full mt-5 p-3 text-white' type="submit">Submit</button>
        </form>

      )}
      
    </div>
  );
};

export default FormComponent;
