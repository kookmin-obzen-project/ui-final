import React, { useState, useEffect } from 'react';

interface HeaderProps {}

const Header: React.FC<HeaderProps> = () => {
  const [currentTime, setCurrentTime] = useState<string>(
    formatTime(new Date())
  );

  useEffect(() => {
    const intervalId = setInterval(() => {
      setCurrentTime(formatTime(new Date()));
    }, 1000); 

    return () => clearInterval(intervalId);
  }, []); 

  function formatTime(date: Date): string {
    const hours = date.getHours();
    const minutes = date.getMinutes();

    const period = hours >= 12 ? '오후' : '오전';
    const formattedHours = hours % 12 || 12;
    const formattedMinutes = minutes.toString().padStart(2, '0');

    return `${period} ${formattedHours}:${formattedMinutes}`;
  }

  return (
    <div>
      <div className="h-20 bg-white pb-4">
        <div className="flex h-5 items-center p-10 justify-between">
          <div className="flex lg:flex-1">
            <a href="#!" className="-m-1.5 p-1.5">
              <img
                className="h-9 w-auto"
                src="https://obzen.com/img/logo_red.png"
                alt=""
              />
              <span className="sr-only">Obzen</span>
            </a>
          </div>
          <div className="text-2xl font-bold">{currentTime}</div>
        </div>
      </div>
      <div className="border-b border-default-border"></div>
    </div>
  );
};

export default Header;

