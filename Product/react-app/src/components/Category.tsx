import React from "react";
import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "./Category.css";
import Loader from "./Loader";

interface CategoryProp {
    id: string;
    title: string;
    description: string;
};

interface ProductProp {
    id: string;
    name: string;
    description: string;
    category: string;
    price: number;
};

const Category = () => {
    const { categoryId } = useParams<{ categoryId: string }>();
    const [category, setCategory] = useState<CategoryProp>({} as CategoryProp);
    const [products, setProducts] = useState<ProductProp[]>([]);
    const [loading, setLoading] = useState(true);
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [error, setError] = useState<string | null>(null);
    const URL_BASE = "http://localhost:8000";

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                setError(null);
                
                // Fetch category first
                const categoryResponse = await fetch(`${URL_BASE}/category/?id=${categoryId}`);
                if (!categoryResponse.ok) {
                    throw new Error("Network response was not ok");
                }
                const categoryData = await categoryResponse.json().catch((err) => {
                    console.error(err);
                    throw err; 
                });

                setCategory(categoryData.data || categoryData);
                // Then fetch products for this category
                const productsResponse = await fetch(`${URL_BASE}/products/?category=${categoryId}&page=${page}`);
                if (!productsResponse.ok) {
                    throw new Error("Network response was not ok");
                }
                if('error' in productsResponse){
                    throw new Error(String(productsResponse['error']));
                }

                const productsData = await productsResponse.json().catch((err) => {
                    console.error(err);
                    throw err;
                });
                
                setProducts(productsData['products'] || productsData);
                setTotalPages(productsData.total_pages || 1);
                
            } catch (err) {
                if (err instanceof Error) {
                    setError(err.message);
                } else {
                    setError("An unexpected error occurred");
                }
            } finally {
                setLoading(false);
            }
        };
        
        fetchData();
    }, [page]);

    if (loading) return <Loader/>;
    if (error) return <div>Error: {error}</div>;

    return (
        <>
            <div className="category-header" >
                <h2>{category.title}</h2>
            </div>
            <div className="category-container">
                <h3>Products in this category</h3>
                {products.length > 0 ? (
                    <>
                    <ul className="product-list">
                        {products.map((product) => (
                            <li key={product.id} className="product-item">
                                <h4>{product.name}</h4>
                                <p>{product.description}</p>
                            </li>
                        ))}
                    </ul>
                    <div className="pagination">
                    <button disabled= {page === 1} onClick={() => setPage(page - 1)}>
                        Previous
                    </button>
                    <span>Page {page} of {totalPages}</span>
                    <button disabled={page === totalPages} onClick={() => setPage(page + 1)}>
                        Next
                    </button>
                </div>    
            </>
            ) : (
                    <p className="no-product">No products found in this category.</p>
                )}
            </div>
        </>
    );
};

export default Category;