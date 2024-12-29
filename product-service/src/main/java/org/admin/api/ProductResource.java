package org.admin.api;

import jakarta.transaction.Transactional;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import org.admin.model.Product;
import io.dapr.client.DaprClient;
import io.dapr.client.DaprClientBuilder;

import java.util.HashMap;
import java.util.Map;

@Path("/product")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class ProductResource {

    private static final String SQL_BINDING_NAME = "mysql-binding"; // Nom du binding Dapr configuré dans Dapr

    // Créez un client Dapr pour communiquer avec les bindings
    DaprClient client = new DaprClientBuilder().build();

    // Ajouter un nouveau produit via Dapr Binding
    @POST
    @Transactional
    public Response addProduct(Product product) {
        // Créez la requête SQL avec String.format
        String sql = String.format("INSERT INTO products (name, price, stock) VALUES ('%s', %f, %d)",
                product.getName(), product.getPrice(), product.getStock());

        Map<String, String> metadata = new HashMap<>();
        metadata.put("sql", sql); // Ajoutez la requête SQL dans les métadonnées

        try {
            // Utiliser le Dapr client pour invoquer le binding avec l'opération "exec"
            client.invokeBinding(SQL_BINDING_NAME, "exec", null, metadata).block();
            return Response.status(Response.Status.CREATED).entity("{\"status\": \"Product created\"}").build();
        } catch (Exception e) {
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                    .entity(e.getMessage())
                    .build();
        }
    }

    // Obtenir un produit par ID via Dapr Binding
    @GET
    @Path("/get/{id}")
    public Response getProduct(@PathParam("id") Long id) {
        String sql = String.format("SELECT * FROM products WHERE id = %d", id);
        Map<String, String> metadata = new HashMap<>();
        metadata.put("sql", sql);

        try {
            // Appeler le binding Dapr pour obtenir les données
            byte[] productDataBytes = client.invokeBinding(SQL_BINDING_NAME, "query", null, metadata).block();
            if (productDataBytes == null) {
                return Response.status(Response.Status.NOT_FOUND).build();
            }
            String productData = new String(productDataBytes);
            return Response.ok(productData).build();
        } catch (Exception e) {
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                    .entity(e.getMessage())
                    .build();
        }
    }

    // Mettre à jour un produit via Dapr Binding
    @PUT
    @Path("/update/{id}")
    @Transactional
    public Response updateProduct(@PathParam("id") Long id, Product updatedProduct) {
        String sql = String.format("UPDATE products SET name = '%s', price = %f, stock = %d WHERE id = %d",
                updatedProduct.getName(), updatedProduct.getPrice(), updatedProduct.getStock(), id);

        Map<String, String> metadata = new HashMap<>();
        metadata.put("sql", sql);

        try {
            client.invokeBinding(SQL_BINDING_NAME, "exec", null, metadata).block();
            return Response.ok("{\"status\": \"Product updated\"}").build();
        } catch (Exception e) {
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                    .entity(e.getMessage())
                    .build();
        }
    }

    // Supprimer un produit via Dapr Binding
    @DELETE
    @Path("/delete/{id}")
    @Transactional
    public Response deleteProduct(@PathParam("id") Long id) {
        String sql = String.format("DELETE FROM products WHERE id = %d", id);

        Map<String, String> metadata = new HashMap<>();
        metadata.put("sql", sql);

        try {
            client.invokeBinding(SQL_BINDING_NAME, "exec", null, metadata).block();
            return Response.noContent().build();
        } catch (Exception e) {
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                    .entity(e.getMessage())
                    .build();
        }
    }
}
