import { useParams } from "react-router-dom";

export default function EeocByPersonId() {
  // ใช้ useParams ดึงค่า paramId จาก URL ค่า~
  const { paramId } = useParams<{ paramId: number }>();

  return (
    <div>
      <p>Person ID: {paramId}</p>
    </div>
  );
}