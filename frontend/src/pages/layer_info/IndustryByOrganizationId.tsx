import React from "react";
import { useParams } from "react-router-dom";

function IndustryByOrganizationId() {
  const { paramId } = useParams<{ paramId: string }>();
  return <div>IndustryByOrganizationId {paramId}</div>;
}

export default IndustryByOrganizationId;
