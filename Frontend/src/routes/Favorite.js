import { dbService } from "fbase";
import { useEffect, useState } from "react";
import CategoryPage from "./CategoryPage";

const Favorite = ({ userObj }) => {
  const [userArray, setUserArray] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState("");
  const [chosen, setChosen] = useState(false);
  const loadUsers = async () => {
    let data = await dbService.collection("category").get();
    for (const doc of data.docs) {
      if (doc.id === userObj.uid) {
        setUserArray(doc.data().categorys);
      }
    }
    setLoading(false);
  };

  useEffect(() => {
    loadUsers();
  }, []);

  const SelectBox = (props) => {
    const handleChange = (event) => {
      setSelected(event.target.value);
      setChosen(true);
    };

    return (
      <select onChange={handleChange} value={selected}>
        <option defaultValue="default">=== 선택 ===</option>
        {props.options.map((category) => (
          <option value={category} key={category}>
            {category}
          </option>
        ))}
      </select>
    );
  };

  return (
    <div className="container">
      <h1 className="intro">나만의 관심 카테고리!</h1>
      <h2 className="text">프로필에서 나만의 관심 카테고리를 설정해보세요!</h2>
      <br></br>
      <SelectBox options={userArray}></SelectBox>
      {chosen ? (
        <CategoryPage category={selected} />
      ) : (
        <h1>카테고리를 선택해보세요!</h1>
      )}
    </div>
  );
};

export default Favorite;
