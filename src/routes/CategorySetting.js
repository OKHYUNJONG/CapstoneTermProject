import { dbService } from "fbase";
import { useEffect, useState } from "react";

const CategorySetting = ({ userObj }) => {
  const categoryList = [
    "먹거리",
    "디지털/게임",
    "디지털/공유기",
    "디지털/기타",
    "디지털/노트북",
    "디지털/데스크탑",
    "디지털/마우스",
    "디지털/메모리",
    "디지털/모니터",
    "디지털/보조배터리",
    "디지털/블랙박스",
    "디지털/선풍기",
    "디지털/세탁기",
    "디지털/스피커",
    "디지털/시계",
    "디지털/에어컨",
    "디지털/외장하드",
    "디지털/이어폰",
    "디지털/제습기",
    "디지털/청소기",
    "디지털/충전기",
    "디지털/카메라",
    "디지털/케이블",
    "디지털/케이스",
    "디지털/키보드",
    "디지털/태블릿",
    "디지털/TV",
    "디지털/프린터",
    "디지털/핸드폰",
    "디지털/헤드폰",
    "디지털/SD카드",
    "디지털/SSD",
  ];
  const [categorys, setCategorys] = useState(new Set());

  const checkedItemHandler = (event) => {
    if (event.target.checked) {
      categorys.add(event.target.value);
      setCategorys(categorys);
    } else if (!event.target.checked && categorys.has(event.target.value)) {
      categorys.delete(event.target.value);
      setCategorys(categorys);
    }
  };

  const onSubmit = async (event) => {
    event.preventDefault();
    const arr = [...categorys];
    await dbService.collection("category").doc(userObj.uid).set({
      categorys: arr,
    });
    document.location.href = "/";
  };

  return (
    <div className="container">
      <h2 className="intro">관심있는 제품을 선택해보세요!</h2>
      <form onSubmit={onSubmit}>
        {categoryList.map((category) => (
          <div key={category}>
            <label class="checkContainer">
              <input
                type="checkbox"
                value={category}
                onChange={(event) => {
                  checkedItemHandler(event);
                }}
                id={category}
              />
              {category}
              <span class="checkmark"></span>
            </label>

            <br></br>
          </div>
        ))}

        <input type="submit" value="저장!" className="save" />
      </form>
    </div>
  );
};

export default CategorySetting;
