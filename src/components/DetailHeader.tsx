import React, { useState } from "react";
import ReactDOM from "react-dom"; 

interface DetailHeaderProps {
  detailInfo: string;
}

const DetailHeader: React.FC<DetailHeaderProps> = ({ detailInfo }) => {
  const [isPopupOpen, setIsPopupOpen] = useState(false);

  const openPopup = () => {
    setIsPopupOpen(true);
  };

  const closePopup = () => {
    setIsPopupOpen(false);
  };

  const sampleSQLQuery = "SELECT * FROM users WHERE age > 18;"; // 예시 SQL 쿼리

  return (
    <div className="flex justify-between items-center my-3">
      <div className="">
        <span className="text-detail-black font-bold">{detailInfo}</span>
        <span className="text-obzen-purple font-bold mx-2">2422</span>
        <span>명</span>
      </div>
      <button className="text-default-blue font-bold" onClick={openPopup}>
        SQL 보기
      </button>

      {/* 팝업 */}
      {isPopupOpen && ReactDOM.createPortal(
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-white p-4 rounded-lg shadow-md">
            <h2 className="text-lg font-semibold mb-2">SQL 쿼리</h2>
            <pre className="bg-gray-100 p-2 rounded-lg overflow-auto">
              {sampleSQLQuery}
            </pre>
            <button className="text-default-blue font-bold mt-4" onClick={closePopup}>
              닫기
            </button>
          </div>
        </div>,
        document.body 
      )}
    </div>
  );
};


export default DetailHeader;