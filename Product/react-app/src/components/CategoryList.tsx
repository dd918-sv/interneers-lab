import React from "react";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./CategoryList.css";
import Loader from "./Loader";

interface CategoryProp {
    id: string;
    title: string;
    description: string;
}

const CategoryList = () => {
    const [categories, setCategories] =useState<CategoryProp[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const navigate = useNavigate();
    const URL_BASE = "http://localhost:8000";
    
    useEffect(() => {
        const fetchCategories = async () => {
            try {
                setLoading(true);
                setError(null);
                await new Promise(resolve => setTimeout(resolve, 50));
                const response = await fetch(`${URL_BASE}/category/?page=${page}`);
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                const data = await response.json().catch((err) => {
                    console.error(err);
                    throw err;
                });
                if(data['success'] === false){
                    throw new Error(data['message']);
                } else {

                    setCategories(data['data'].categories || data['data']);
                    setTotalPages(data['data'].total_pages || 1);
                    setLoading(false);
                } 
            } catch (err) {
                if (err instanceof Error) {
                    setError(err.message);
                    setLoading(false);
                } else {
                    setError("An unexpected error occurred");
                    setLoading(false);
                }
            }
        };
        fetchCategories();
    }, [page]);

    const handleCategoryClick = async (categoryId: string) => {
        navigate(`/category/${categoryId}`);
    };

    if (loading) return <Loader />;
    if (error) return <div>Error: {error}</div>;

    return (
        <div className="category-container">
      <h1>Category List</h1>
      <div className="category-list">
        {categories.map((category: CategoryProp) => (
          <div
            key={category.id}
            className="category-item"
            onClick={() => handleCategoryClick(category.id)}
          >
            <h3>{category.title}</h3>
            <p>ID: {category.id}</p>
            <p>Description: {category.description}</p>
          </div>
        ))}
      </div>

      <div className="pagination">
        <button
          disabled={page === 1}
          onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
        >
          Previous
        </button>

        <span>
          Page {page} of {totalPages}
        </span>
        <button
          disabled={page === totalPages}
          onClick={() => setPage((prev) => Math.min(prev + 1, totalPages))}
        >
          Next
        </button>
      </div>
    </div>
    );
};

export default CategoryList;