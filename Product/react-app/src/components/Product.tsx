import React from "react";

interface ProductProps {
  product: {
    name: string;
    id: string;
    description: string;
    quantity: number;
    price: number;
    brand?: string;
    "category-title"?: string;
  };
  isSummary: boolean;
}

const Product = ({ product, isSummary }: ProductProps) => {
  if (!product) return null;

  return (
    <div className={`product ${isSummary ? "summary" : "detail"}`}>
      {isSummary ? (
        <>
          <h3>{product.name}</h3>
          <p>Quantity: {product.quantity}</p>
          <p>Price: ${product.price}</p>
        </>
      ) : (
        <>
          <h2>{product.name}</h2>
          <p>
            <strong>ID:</strong> {product.id}
          </p>
          <p>
            <strong>Description:</strong>${product.description}
          </p>
          <p>
            <strong>Quantity:</strong>{product.quantity}
          </p>
          <p>
            <strong>Price:</strong>${product.price}
          </p>
          <p>
            <strong>Brand:</strong>
            {product.brand}
          </p>
          <p>
            <strong>Category:</strong>
            {product["category-title"]}
          </p>
        </>
      )}
    </div>
  );
};
export default Product;
