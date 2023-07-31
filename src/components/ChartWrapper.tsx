import React from "react";

type ChartWrapperProps = {
  childern: React.ReactNode;
};

export default function ChartWrapper({ childern }: ChartWrapperProps) {
  return <div className="border h-96">{childern}</div>;
}
