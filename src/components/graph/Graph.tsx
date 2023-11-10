import React from "react";
import BarChart from "./BarChart";
import { BarDatum } from "@nivo/bar";
import DetailHeader from "./DetailHeader";
import { FaCircleNotch } from "react-icons/fa";

interface GraphProps {
  isGraphLoading: boolean;
  query : string;
}

const Graph: React.FC<GraphProps> = ({ isGraphLoading, query }) => {
  return (
    <div className="px-6 py-2 flex flex-col">
      <DetailHeader
        detailInfo={
          isGraphLoading
            ? "" // 로딩 중일 때 빈 문자열로 처리
            : "최근 1개월동안 모바일 앱에 접속하지 않은 고객은"
        }
        query={query}
      />
      {isGraphLoading ? (
        <div className="relative flex items-center justify-center h-48">
          <div className="w-8 h-8 mr-2 text-violet-400 animate-spin">
            <FaCircleNotch />
          </div>
          Loading Graph...
        </div>
      ) : (
        <div className="border px-3 py-1 rounded">
          <span className="text-obzen-purple font-bold my-2 text-lg block">
            성별
          </span>
          <span className="text-detail-black font-bold block">
            남 58.2%, 여 41.8%
          </span>
          <BarChart data={data} />
        </div>
      )}
    </div>
  );
};

// TODO: data should be fetched from the server
const data: BarDatum[] = [
  {
    sex: "남성",
    전체고객: 152,
    "hot dogColor": "hsl(168, 70%, 50%)",
    해당그룹: 50,
    burgerColor: "hsl(111, 70%, 50%)",
  },
  {
    sex: "여성",
    전체고객: 103,
    "hot dogColor": "hsl(310, 70%, 50%)",
    해당그룹: 124,
    burgerColor: "hsl(226, 70%, 50%)",
  },
];

export default Graph;
