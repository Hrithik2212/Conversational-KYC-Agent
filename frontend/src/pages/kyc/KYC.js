import React,{ useState,useEffect } from 'react'
import Dictaphone from '../../components/kyc/audio/Audio'
import Nav from '../../components/nav/Nav'
import VideoCard from '../../components/kyc/videoCard/VideoCard'
import Listen from '../../components/kyc/listen/Listen'
import TextToSpeech from '../../components/kyc/textToSpeech/TextToSpeech'
import QuestionCard from '../../components/kyc/questionCard/QuestionCard'
import Instructions from '../../components/kyc/instructions/Instructions'
import FormComponent from '../../components/kyc/form/Form'
const KYC = () => {
    const [questions,setQuestions]=useState([])
    const [question,setQuestion]=useState([])
    const [data,setData]=useState(null)

    useEffect(()=>{
      const fetchquestions=async()=>{
        let response=await fetch('http://127.0.0.1:8000/getquestions') 
        if(response.ok) {
          const res=await response.json()
          setQuestions(res?.questions)
          const initialQuestions = res?.questions.reduce((acc, item) => {
            acc[item.label] = ""
            return acc;
          }, {});
          setData(initialQuestions)
        }   
         
      }
      fetchquestions()
    },[])
    const changeQuestion = ()=>{
      let index=question.key + 1
      if(index <=  questions.length - 1){
        setQuestion({
          "key": index,
          "value": questions[index]?.question,
          "label":questions[index]?.label,
          "speak":questions[index]?.speak
        });
      }
      else{
        setQuestion({
          "key": index,
          "value": "Completed"
        });

      }

    }
    

    useEffect(()=>{
      
      setQuestion({
        "key": 0,
        "value": "Completed",
        "label":questions[0]?.label,
        "speak":questions[0]?.speak
      });
      

    },[questions])
  

  return (
    <div className='min-h-[100vh] flex flex-col items-center'>
      
      <div className=' w-full top-0'>
          <Nav />
      

      </div>
      
    <Instructions/>
      

      


        <div className='flex  h-full mt-0 flex-1 w-full max-w-[1600px]  '>
            <div className='w-[70%] flex justify-center items-center'>
                <div className='w-[30%]'>
                  {question?.value === "Completed" ? (<FormComponent data={data} setData={setData}/>):(<Dictaphone question={question} changeQuestion={changeQuestion} setData={setData}/>)}
                    
                </div>
            </div>
           

            <div className='w-[30%] min-w-[300px] flex flex-col  justify-stretch  items-center'>
              
                  <QuestionCard question={question?.value}/>
             
                
                <div className='min-w-[300px] min-h-[200px] h-full w-full  max-w-[500px]  max-h-[300px]'>
                    <VideoCard/>
                </div>
            </div>

        </div>
        
      
        
    </div>
  )
}

export default KYC