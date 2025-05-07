import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import ProductList from "./components/ProductList";
import Home from "./components/Home";
import UpdateProduct from "./components/UpdateProduct";
import CategoryList from "./components/CategoryList";
import Category from "./components/Category";

import "./App.css";

function App() {
  return (
    <Router>
      <div className="app">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/products" element={<ProductList />} />
            <Route path="/products/update/:productId" element={<UpdateProduct />} />
            <Route path="/category" element={<CategoryList />} />
            <Route path="/category/:categoryId" element={<Category />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
