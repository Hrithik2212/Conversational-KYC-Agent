import Image from 'next/image'
import Button from './Button'
import Link from 'next/link';

const Hero = () => {
  return (
    <section className="max-container padding-container flex flex-col gap-20 py-10 pb-32 md:gap-28 lg:py-20 xl:flex-row">
      <div className="hero-map" />

      <div className="relative z-20 flex flex-1 flex-col xl:w-1/2">
        <Image
          src="/Default_elements_such_as_identity_verification_documents_digi_0-removebg-preview.png"
          alt="ai-image"
          width={70}
          height={70}
          className="absolute left-[-5px] top-[-30px] w-10 lg:w-[50px]"
        />
        <h1 className="bold-52 lg:bold-88">KYC made easy..</h1>
        <p className="regular-16 mt-6 text-gray-30 xl:max-w-[520px]">
          We're with you every step, ensuring secure identity verification. Our app offers liveliness detection, face verification, multi-lingual support, and voice-based guidance for seamless KYC compliance.
        </p>

        <div className="my-11 flex flex-wrap gap-5">
          <div className="flex items-center gap-2">
            {Array(5).fill(1).map((_, index) => (
              <Image
                src="/star.svg"
                key={index}
                alt="star"
                width={24}
                height={24}
              />
            ))}
          </div>

          <p className="bold-16 lg:bold-20 text-blue-70">
            20,000
            <span className="regular-16 lg:regular-20 ml-1">KYC's completed.</span>
          </p>
        </div>

        <div className="flex flex-col w-full gap-3 sm:flex-row">
          <Link href="/demo">
            <Button
              type="button"
              title="Try Demo"
              variant="btn_green"
            />
          </Link>
          <Link href="/demo">
            <Button
              type="button"
              title="Enterprise Solutions"
              icon="/icons8-play-button-96.png"
              variant="btn_white_text"
            />
          </Link>
        </div>
      </div>

      <div className="relative flex flex-1 items-start">
        <div className="relative z-20 flex w-[268px] flex-col gap-8 rounded-3xl bg-green-90 px-7 py-8">

          <div className="flex flex-col">
            <div className="flexBetween">
              <p className="regular-16 text-gray-20">Know Your Customer</p>
              <Image src="/close.svg" alt="close" width={24} height={24} />
            </div>
            <p className="bold-20 text-white">SRM</p>
          </div>

          <div className="flexBetween">
            <div className="flex flex-col">
              <p className="regular-16 block text-gray-20">Aadhar</p>
              <p className="bold-30 text-white">xxxxxxxxxxxx</p>
            </div>
            <div className="flex flex-col">
              <p className="regular-16 block text-gray-20">PAN</p>
              <p className="bold-30 text-white">XXXX0000X</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Hero