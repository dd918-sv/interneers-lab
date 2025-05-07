import React from 'react';
import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import './UpdateProduct.css';
import { useNavigate } from 'react-router-dom';
import Loader from './Loader';

interface ProductProp {
    name: string;
    id: string;
    description: string;
    price: number;
    brand?: string;
    quantity: number;
    "category-title"?: string;
}
const URL_BASE = "http://localhost:8000";

const UpdateProduct = () => {
    const { productId } = useParams();
    const [product, setProduct] = useState<ProductProp | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [formData, setFormData] = useState<ProductProp | null>(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProduct = async () => {
            try {
                const response = await fetch(`${URL_BASE}/products/?id=${productId}`);
                if(!response.ok) {
                    throw new Error("Network response was not ok");
                }
                const data = await response.json();
                const req_data=data['data'];
                setProduct(req_data);
                setFormData(req_data);
                setLoading(false);
            } catch(err) {
                if (err instanceof Error) {
                    setError(err.message);
                    setLoading(false);
                } else {
                    setError("An unexpected error occurred");
                    setLoading(false);
                }
            }
        };
        fetchProduct();
    },[]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const response = await fetch(`${URL_BASE}/products/?id=${productId}`,{
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });
            console.log(response);
            const result = await response.json();
            if(response.ok) {
                if(result['success']){
                    setProduct(result['data']);
                    alert("Product updated successfully");
                    navigate('/products');
                } else {
                    alert("Product not updated:" + result.message);
                }
            } else {
                throw new Error(result.message || "Failed to update product");
            }
        } catch (err) {
            if (err instanceof Error) {
                alert(err.message);
            } else {
                setError("An unexpected error occurred");
            }
        }
    }



    return (
        <div className = "update-box">
            <h1>Update Product</h1>
            {loading && <Loader/>}
            {/* {error && <p>{error}</p>} */}
            {product && formData && (
                <form className="form-container" onSubmit={handleSubmit}>
                    <label>
                        Product Name:
                        <input type="text" defaultValue={product['name']} id="form-name" value={formData['name']} disabled/>
                    </label>
                    <label>
                        Product Id:
                        <input type="text" defaultValue={product['id']} id="form-id" value={formData['id']} disabled/>
                    </label>
                    <label>
                        Product Description: 
                        <input type="text" defaultValue={product['description']} placeholder="Description" value={formData['description']} id="form-description" onChange= {(e) => setFormData({ ...formData,description: e.target.value })} />
                    </label>
                    <label>
                        Product Price: 
                        <input type="number" defaultValue={product['price']} placeholder="Enter price in number" value={formData['price']} id="form-price" onChange= {(e) => setFormData({ ...formData,price: Number(e.target.value) })} />
                    </label>
                    <label>
                        Product Quantity:
                        <input type ="number" defaultValue={product['quantity']} placeholder="Enter quantity in number" value={formData['quantity']} id="form-quantity" onChange = {(e) => setFormData({ ...formData,quantity: Number(e.target.value) })} />
                    </label>
                    <label>
                        Product Brand:
                        <input type="text" defaultValue={product['brand']} placeholder="Brand" value={formData['brand']} id="form-brand" onChange= {(e) => setFormData({ ...formData,brand: e.target.value })} />
                    </label>
                    <label>
                        Product Category:
                        <input type="text" defaultValue={product['category-title']} placeholder="Category" value={formData['category-title']} id="form-category" onChange= {(e) => setFormData({ ...formData,"category-title": e.target.value })}/>
                    </label>
                   <button type="submit">Update</button>
                </form>
            )}
        </div>
    );


};

export default UpdateProduct;