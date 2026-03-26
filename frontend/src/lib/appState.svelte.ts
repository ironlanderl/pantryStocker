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
    endpoint = "127.0.0.1:8000"
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
            const response = await fetch(`http://${this.endpoint}/locations/`);
            if (response.ok) {
                this.locations = await response.json();
                console.log(this.locations);
            }
        } catch (error) {
            console.error("Failed to fetch locations:", error);
        }
    }
}

export const appState = new AppState();
