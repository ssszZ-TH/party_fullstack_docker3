import { useEffect } from "react";
import {
  create,
  deleteById,
  get,
  list,
  update,
} from "../services/maritalstatustype";

function Users() {
  useEffect(() => {
    list().then(data => console.log(data));
  }, []);

  return (
    <>
      <div>Users</div>
    </>
  );
}

export default Users;
