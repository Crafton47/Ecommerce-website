import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpExchange;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.util.HashMap;
import java.util.Map;

public class CurrencyServer {

    // Fixed exchange rates relative to INR
    static final Map<String, Double> RATES = new HashMap<>();

    static {
        RATES.put("USD", 0.012);
        RATES.put("EUR", 0.011);
        RATES.put("GBP", 0.0095);
        RATES.put("JPY", 1.78);
        RATES.put("INR", 1.0);
    }

    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);

        // GET /convert?amount=1000&to=USD
        server.createContext("/convert", (HttpExchange exchange) -> {
            // Allow CORS so Flask can call this
            exchange.getResponseHeaders().add("Access-Control-Allow-Origin", "*");
            exchange.getResponseHeaders().add("Content-Type", "application/json");

            String response;

            try {
                String query = exchange.getRequestURI().getQuery();
                Map<String, String> params = parseQuery(query);

                double amount = Double.parseDouble(params.getOrDefault("amount", "0"));
                String to = params.getOrDefault("to", "USD").toUpperCase();

                if (!RATES.containsKey(to)) {
                    response = "{\"error\":\"Unsupported currency: " + to + "\"}";
                } else {
                    double converted = amount * RATES.get(to);
                    String symbol = getSymbol(to);
                    response = String.format(
                        "{\"from\":\"INR\",\"to\":\"%s\",\"amount\":%.2f,\"converted\":%.2f,\"symbol\":\"%s\"}",
                        to, amount, converted, symbol
                    );
                }
            } catch (Exception e) {
                response = "{\"error\":\"Invalid request\"}";
            }

            byte[] bytes = response.getBytes();
            exchange.sendResponseHeaders(200, bytes.length);
            OutputStream os = exchange.getResponseBody();
            os.write(bytes);
            os.close();
        });

        server.start();
        System.out.println("✅ Currency API running at http://localhost:8080/convert");
        System.out.println("   Example: http://localhost:8080/convert?amount=79900&to=USD");
    }

    static Map<String, String> parseQuery(String query) {
        Map<String, String> map = new HashMap<>();
        if (query == null) return map;
        for (String pair : query.split("&")) {
            String[] kv = pair.split("=");
            if (kv.length == 2) map.put(kv[0], kv[1]);
        }
        return map;
    }

    static String getSymbol(String currency) {
        switch (currency) {
            case "USD": return "$";
            case "EUR": return "€";
            case "GBP": return "£";
            case "JPY": return "¥";
            default:    return "₹";
        }
    }
}
