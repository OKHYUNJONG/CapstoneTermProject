import PropTypes from "prop-types";
import { Link } from "react-router-dom";

function ProductDetail({
  category,
  date,
  place,
  id,
  img,
  link,
  price,
  productName,
  text,
  shopUrl,
}) {
  const imagestyle = {
    height: "30vh",
  };
  const addDefaultImg = (ev) => {
    ev.target.src =
      "https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg";
  };

  return (
    <div>
      <div className="container">
        <h1 className="productName">{productName}</h1>
        <img src={img} onError={addDefaultImg} style={imagestyle} />
        <p>
          {text.map((oneText) => (
            <div className="text">{oneText}</div>
          ))}
          <br></br>
        </p>
      </div>
      <div className="text">
        구매하러 바로 가기 :{" "}
        <a target="_blank" href={shopUrl}>
          {shopUrl}
        </a>
      </div>
      <div className="text">
        원본 링크 :{" "}
        <a target="_blank" href={link}>
          {link}
        </a>
      </div>
    </div>
  );
}

export default ProductDetail;
