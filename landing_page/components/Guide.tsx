import Image from 'next/image'
import React from 'react'

const Guide = () => {
  return (
    <section className="flexCenter flex-col">
      <div className="padding-container max-container w-full pb-24">
        <Image src="/Default_elements_such_as_identity_verification_documents_digi_0-removebg-preview.png" alt="camp" width={50} height={50} />
        <p className="uppercase regular-18 -mt-1 mb-3 text-blue-500">
          We are here for you
        </p>
        <div className="flex flex-wrap justify-between gap-5 lg:gap-10">
          <h2 className="bold-40 lg:bold-64 xl:max-w-[390px]">Guide You to Easy Identification</h2>
          <p className="regular-16 text-gray-30 xl:max-w-[520px]">With our KYC application, we ensure a seamless and secure identity verification process. Our advanced features include liveliness detection, ensuring that the person being verified is physically present and actively participating. Additionally, our face verification technology accurately verifies identities, enhancing security and trust. We offer multi-lingual support, allowing users to verify their identity in their preferred language, making the process accessible to a diverse range of users. Furthermore, our voice-based conversational interface offers a user-friendly experience, guiding you through the verification process with ease. Whether you're online or offline, our application guarantees a reliable and efficient KYC experience, empowering you to achieve your financial goals with confidence.</p>
        </div>
      </div>

      <div className="flexCenter max-container relative w-full">
        <Image
          src="/Default_Create_an_image_depicting_the_process_of_Know_Your_Cus_3.jpg"
          alt="tool"
          width={1440}
          height={580}
          className="w-full object-cover object-center 2xl:rounded-5xl"
        />

        <div className="absolute flex bg-white py-8 pl-5 pr-7 gap-3 rounded-3xl border shadow-md md:left-[5%] lg:top-20">
          <Image
            src="/meter.svg"
            alt="meter"
            width={16}
            height={158}
            className="h-full w-auto"
          />
          <div className="flexBetween flex-col">
            <div className='flex w-full flex-col'>
              <div className="flexBetween w-full">
                <p className="regular-16 text-gray-20">Starting  </p>
                <p className="bold-16 text-blue-500">300 sec</p>
              </div>
              <p className="bold-20 mt-2">Identification</p>
            </div>

            <div className='flex w-full flex-col'>
              <p className="regular-16 text-gray-20">Generated</p>
              <h4 className="bold-20 mt-2 whitespace-nowrap">Identity</h4>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Guide