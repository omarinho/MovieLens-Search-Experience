import { Link } from "react-router-dom";

const NoPage = () => {
  return <h1>404 - Page not found. Go to  <Link to="/">Home</Link></h1>;
};

export default NoPage;