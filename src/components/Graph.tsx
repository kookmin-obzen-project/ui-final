// import React from "react";
import BarChart from "./BarChart";
import { BarDatum } from "@nivo/bar";
import DetailHeader from "./DetailHeader";
// import ChartWrapper from "./ChartWrapper";

export default function Graph() {
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

// TODO: data should be fetched from the server
const data: BarDatum[] = [
  {
    country: "AD",
    "hot dog": 198,
    "hot dogColor": "hsl(78, 70%, 50%)",
    burger: 87,
    burgerColor: "hsl(156, 70%, 50%)",
    sandwich: 61,
    sandwichColor: "hsl(203, 70%, 50%)",
    kebab: 115,
    kebabColor: "hsl(195, 70%, 50%)",
    fries: 100,
    friesColor: "hsl(0, 70%, 50%)",
    donut: 113,
    donutColor: "hsl(171, 70%, 50%)",
  },
  {
    country: "AE",
    "hot dog": 177,
    "hot dogColor": "hsl(280, 70%, 50%)",
    burger: 77,
    burgerColor: "hsl(349, 70%, 50%)",
    sandwich: 166,
    sandwichColor: "hsl(24, 70%, 50%)",
    kebab: 53,
    kebabColor: "hsl(357, 70%, 50%)",
    fries: 9,
    friesColor: "hsl(278, 70%, 50%)",
    donut: 33,
    donutColor: "hsl(308, 70%, 50%)",
  },
  {
    country: "AF",
    "hot dog": 34,
    "hot dogColor": "hsl(353, 70%, 50%)",
    burger: 13,
    burgerColor: "hsl(78, 70%, 50%)",
    sandwich: 134,
    sandwichColor: "hsl(127, 70%, 50%)",
    kebab: 2,
    kebabColor: "hsl(191, 70%, 50%)",
    fries: 4,
    friesColor: "hsl(192, 70%, 50%)",
    donut: 158,
    donutColor: "hsl(236, 70%, 50%)",
  },
  {
    country: "AG",
    "hot dog": 184,
    "hot dogColor": "hsl(240, 70%, 50%)",
    burger: 49,
    burgerColor: "hsl(211, 70%, 50%)",
    sandwich: 155,
    sandwichColor: "hsl(327, 70%, 50%)",
    kebab: 77,
    kebabColor: "hsl(312, 70%, 50%)",
    fries: 175,
    friesColor: "hsl(350, 70%, 50%)",
    donut: 115,
    donutColor: "hsl(178, 70%, 50%)",
  },
  {
    country: "AI",
    "hot dog": 184,
    "hot dogColor": "hsl(126, 70%, 50%)",
    burger: 84,
    burgerColor: "hsl(212, 70%, 50%)",
    sandwich: 48,
    sandwichColor: "hsl(76, 70%, 50%)",
    kebab: 16,
    kebabColor: "hsl(271, 70%, 50%)",
    fries: 51,
    friesColor: "hsl(211, 70%, 50%)",
    donut: 134,
    donutColor: "hsl(41, 70%, 50%)",
  },
  {
    country: "AL",
    "hot dog": 152,
    "hot dogColor": "hsl(168, 70%, 50%)",
    burger: 50,
    burgerColor: "hsl(111, 70%, 50%)",
    sandwich: 73,
    sandwichColor: "hsl(235, 70%, 50%)",
    kebab: 51,
    kebabColor: "hsl(180, 70%, 50%)",
    fries: 157,
    friesColor: "hsl(152, 70%, 50%)",
    donut: 148,
    donutColor: "hsl(314, 70%, 50%)",
  },
  {
    country: "AM",
    "hot dog": 103,
    "hot dogColor": "hsl(310, 70%, 50%)",
    burger: 124,
    burgerColor: "hsl(226, 70%, 50%)",
    sandwich: 99,
    sandwichColor: "hsl(46, 70%, 50%)",
    kebab: 78,
    kebabColor: "hsl(55, 70%, 50%)",
    fries: 129,
    friesColor: "hsl(341, 70%, 50%)",
    donut: 167,
    donutColor: "hsl(269, 70%, 50%)",
  },
];
