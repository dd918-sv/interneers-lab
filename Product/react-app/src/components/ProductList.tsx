import React, { useState, useEffect } from "react";
import { useNavigate} from 'react-router-dom';
import Product from "./Product";
import "./ProductList.css";
import Loader from "./Loader";
const URL_BASE = "http://localhost:8000";

interface ProductProp {
  name: string;
  id: string;
  description: string;
  price: number;
  quantity: number;
  brand?: string;
  "category-title"?: string;
}

const ProductList = () => {
  const [products, setProducts] = useState<ProductProp[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [selectedProduct, setSelectedProduct] = useState<ProductProp | null>(
    null
  );
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        setError(null);
        await new Promise(resolve => setTimeout(resolve, 50));
        const response = await fetch(`${URL_BASE}/products/?page=${page}`);
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json().catch((err) => {
          console.error(err);
          throw err;
      });
        setProducts(data.products || data);
        setTotalPages(data.total_pages || 1);
        setLoading(false);
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

    fetchProducts();
  }, [page]);

  const handleProductClick = async (productId: string) => {
    try {
      const response = await fetch(`${URL_BASE}/products/?id=${productId}`);
      if (!response.ok) {
        throw new Error("Failed to fetch product details");
      }
      const productData = await response.json();
      // console.log(productData);
      setSelectedProduct(productData['data']);
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

  const handleUpdate = async (productId:string) => {
    navigate(`/products/update/${productId}`);
  };

  if (loading) return <Loader/>;
  if (error) return <div>Error...:{error}</div>;

  return (
    <div className="product-container">
      <h1>Product List</h1>
      <div className="product-list">
        {products.map((product: ProductProp) => (
          <div
            key={product.id}
            className="product-item"
            onClick={() => handleProductClick(product.id)}
          >
            <Product product={product} isSummary={true} />
          </div>
        ))}
      </div>

      {selectedProduct && (
        <div className="product-detail">
          <button id="close-btn" onClick={() => setSelectedProduct(null)}>Close</button>
          <Product product={selectedProduct} isSummary={false} />
          <button id="update-btn" onClick={() => handleUpdate(selectedProduct.id)}>Update</button>
        </div>
      )}
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

export default ProductList;
