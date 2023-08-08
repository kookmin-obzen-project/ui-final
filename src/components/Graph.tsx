// import React from "react";
import BarChart from "./BarChart";
// import { BarDatum } from "@nivo/bar";
import DetailHeader from "./DetailHeader";
import { useEffect, useState } from "react";
// import ChartWrapper from "./ChartWrapper";
export default function Graph() {
  const [data, setData] = useState([]);
  useEffect(() => {
    fetchData();
  }, []);
  async function fetchData() {
    try {
      const response = await fetch("http://43.202.78.244:5001");
      const jsonData = await response.json();
      setData(jsonData);
    } catch (error) {
      console.error("데이터를 가져오는데 실패했습니다:", error);
    }
  }
  return (
    // TODO: resize parent height
    <div className="px-6 py-2">
      <DetailHeader
        detailInfo={"최근 1개월동안 모바일 앱에 접속하지 않은 고객은"}
      />
      <BarChart data={data} />
    </div>
  );
}
