import Nweet from "components/Nweet";
import { dbService } from "fbase";
import React, { useEffect, useState } from "react";
import Product from "components/Product";

const Home = ({ userObj }) => {
  let today = new Date();
  let year = today.getFullYear();
  let month = today.getMonth();
  let day = today.getDate();
  let yesterday = new Date(year, month, day - 1);
  let yesYear = yesterday.getFullYear();
  let yesMonth = yesterday.getMonth();
  let yesDay = yesterday.getDate();
  const yesterdayDate = () => {
    let yearString = yesYear.toString();
    let monthString = "";
    let dayString = "";
    if (yesMonth + 1 < 10) {
      monthString = "0" + (yesMonth + 1).toString();
    } else {
      monthString = (yesMonth + 1).toString();
    }
    if (yesDay < 10) {
      dayString = "0" + yesDay.toString();
    } else {
      dayString = yesDay.toString();
    }
    const dateString = yearString + monthString + dayString;
    return dateString;
  };

  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const getProducts = async () => {
    const yesDate = yesterdayDate();
    const json = await (
      await fetch(
        `http://ec2-3-144-12-246.us-east-2.compute.amazonaws.com:5000/posts/${yesDate}`
      )
    ).json();

    setProducts(json);
    setLoading(false);
  };

  useEffect(() => {
    getProducts();
  }, []);

  return (
    <div className="container">
      <div>
        {loading ? (
          <h1>Loading..</h1>
        ) : (
          <div>
            <div style={{ marginTop: 30 }}>
              <h1 style={{ marginBottom: 20 }} className="intro">
                어제({yesYear}-{yesMonth + 1}-{yesDay}) 올라온 핫딜!
              </h1>
              {products.map((product) => (
                <Product
                  key={product.id}
                  category={product.category}
                  place={product.hotdeal_place}
                  id={product.id}
                  time={product.time}
                  title={product.title}
                  img={product.img_url}
                />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
export default Home;
