export enum Operation {
    Scanning = "scanning",
    Lookup = "lookup",
    AddNew = "add_new_product",
    Manage = "manage_existing",
}

class Product {
    id;
    name;
    description;
}

class AppState {
    operation = $state(Operation.Scanning);
    barcode = $state("");
    product = $state(new Product);
    locations = $state([]);

    setProductName(name: string) {
        this.product.name = name;
    }
    
    setProductDesc(desc: string) {
        this.product.description = desc;
    }

    setOperation(op: Operation) {
        this.operation = op;
    }

    setBarcode(code: string) {
        this.barcode = code;
        this.product.id = code;
    }

    async fetchLocations() {
        try {
            const response = await fetch("http://192.168.178.26:8000/locations/");
            if (response.ok) {
                this.locations = await response.json();
            }
        } catch (error) {
            console.error("Failed to fetch locations:", error);
        }
    }
}

export const appState = new AppState();
