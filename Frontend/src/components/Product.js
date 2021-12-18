import PropTypes from "prop-types";
import { Link } from "react-router-dom";

function Product({ category, date, place, id, img, time, title }) {
  const ColoredLine = ({ color }) => (
    <hr
      style={{
        color: color,
        backgroundColor: color,
        height: 0.5,
      }}
    />
  );
  const imagestyle = {
    height: "30vh",
  };
  const addDefaultImg = (ev) => {
    ev.target.src =
      "https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg";
  };
  const divstyle = {};
  return (
    <div>
      <img
        src={img}
        alt="default image"
        onError={addDefaultImg}
        style={imagestyle}
      />
      <div>
        <h4 className="productName">
          <Link to={`/product/${id}`}> {title} </Link>
        </h4>
        <div>카테고리 : {category}</div>
        <div>판매처 : {place}</div>
      </div>
      <ColoredLine color="black" />
    </div>
  );
}

export default Product;
