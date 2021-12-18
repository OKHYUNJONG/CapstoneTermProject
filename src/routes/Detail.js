import Return from "../components/Return";
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import ProductDetail from "components/ProductDetail";

function Detail() {
  const { id } = useParams();
  const [product, setProduct] = useState([]);
  const [loading, setLoading] = useState(true);

  const getProduct = async () => {
    const json = await (
      await fetch(
        `http://ec2-3-144-12-246.us-east-2.compute.amazonaws.com:5000/post/${id}`
      )
    ).json();
    setProduct(json);
    setLoading(false);
  };
  useEffect(() => {
    getProduct();
  }, []);
  return (
    <div>
      {loading ? (
        <h1>Loading..</h1>
      ) : (
        <div>
          <ProductDetail
            key={product[0].id}
            category={product[0].category}
            date={product[0].date}
            place={product[0].hotdeal_place}
            id={product[0].id}
            img={product[0].img_url}
            link={product[0].link}
            price={product[0].price}
            productName={product[0].title}
            text={product[0].text}
            shopUrl={product[0].shop_url}
          />
        </div>
      )}
      <Return />
    </div>
  );
}
export default Detail;
