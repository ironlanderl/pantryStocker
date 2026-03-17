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
}

export const appState = new AppState();
