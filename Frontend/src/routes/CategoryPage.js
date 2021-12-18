import Nweet from "components/Nweet";
import { dbService } from "fbase";
import React, { useEffect, useState } from "react";
import Product from "components/Product";

const CategoryPage = ({ category }) => {
  let today = new Date();
  let year = today.getFullYear();
  let month = today.getMonth();
  let day = today.getDate();
  let yesterday = new Date(year, month, day - 1);
  let yesYear = yesterday.getFullYear();
  let yesMonth = yesterday.getMonth();
  let yesDay = yesterday.getDate();
  let lastMonth = new Date(year, month - 1, day - 1);
  let lastMonthYear = lastMonth.getFullYear();
  let lastMonthMonth = lastMonth.getMonth();
  let lastMonthDay = lastMonth.getDate();
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
  const lastMonthDate = () => {
    let yearString = lastMonthYear.toString();
    let monthString = "";
    let dayString = "";
    if (yesMonth + 1 < 10) {
      monthString = "0" + (lastMonthMonth + 1).toString();
    } else {
      monthString = (lastMonthMonth + 1).toString();
    }
    if (yesDay < 10) {
      dayString = "0" + lastMonthDay.toString();
    } else {
      dayString = lastMonthDay.toString();
    }
    const dateString = yearString + monthString + dayString;
    return dateString;
  };
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const getProducts = async () => {
    setLoading(true);
    const yesDate = yesterdayDate();
    const lastMonDate = lastMonthDate();
    const json = await (
      await fetch(
        `http://ec2-3-144-12-246.us-east-2.compute.amazonaws.com:5000/termposts/${lastMonDate}${yesDate}/${category}`
      )
    ).json();

    setProducts(json);
    setLoading(false);
  };

  useEffect(() => {
    getProducts();
  }, [category]);

  return (
    <div className="container">
      <div>
        {loading ? (
          <h1>Loading..</h1>
        ) : (
          <div>
            <h3 className="intro">
              한 달간({lastMonthYear}-{lastMonthMonth + 1}-{lastMonthDay} ~{" "}
              {yesYear}-{yesMonth + 1}-{yesDay}) 올라온 {category}!
            </h3>
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
        )}
      </div>
    </div>
  );
};

export default CategoryPage;
