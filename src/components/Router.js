import React, { useState } from "react";
import { HashRouter as Router, Route, Switch } from "react-router-dom";
import Profile from "routes/Profile";
import Auth from "../routes/Auth";
import Home from "../routes/Home";
import Navigation from "./Navigation";
import { Redirect } from "react-router";
import Detail from "routes/Detail";
import CategorySetting from "routes/CategorySetting";
import Favorite from "routes/Favorite";
import CategoryPage from "routes/CategoryPage";

const AppRouter = ({ isLoggedIn, userObj }) => {
  return (
    <Router>
      {isLoggedIn && <Navigation />}
      <Switch>
        {isLoggedIn ? (
          <>
            <Route exact path="/">
              <Home userObj={userObj} />
            </Route>
            <Route exact path="/category">
              <CategorySetting userObj={userObj} />
            </Route>
            <Route exact path="/favorite">
              <Favorite userObj={userObj} />
            </Route>
            <Route exact path="/profile">
              <Profile />
            </Route>
            <Route exact path="/product/:id">
              <Detail />
            </Route>
            <Redirect from="*" to="/" />
          </>
        ) : (
          <>
            <Route exact path="/">
              <Auth />
            </Route>
            <Redirect from="*" to="/" />
          </>
        )}
      </Switch>
    </Router>
  );
};
export default AppRouter;
