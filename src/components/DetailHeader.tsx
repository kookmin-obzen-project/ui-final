import React, { useState } from "react";

interface DetailHeaderProps {
  detailInfo: string;
}

const DetailHeader: React.FC<DetailHeaderProps> = ({ detailInfo }) => {
  // const number = detailInfo
  // TODO: 어떻게 숫자만 파싱할 지 고민해야 함.
  // TODO: 어떤 그래프가 필요한 지

  return (
    <div className="flex justify-between items-center  my-3">
      <div className="">
        <span className="text-detail-black  font-bold">{detailInfo}</span>
        <span className="text-obzen-purple font-bold mx-2">2422</span>
        <span>명</span>
      </div>
      <button className="text-default-blue font-bold">SQL 보기</button>
    </div>
  );
};
export default DetailHeader;
