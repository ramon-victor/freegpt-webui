import {Chat, ChatOptions} from "./base";
import {Forefrontnew} from "./forefront";

export enum Model {
    Forefront = 'forefront',
}

export class ChatModelFactory {
    private modelMap: Map<Model, Chat>;
    private readonly options: ChatOptions | undefined;

    constructor(options?: ChatOptions) {
        this.modelMap = new Map();
        this.options = options;
        this.init();
    }

    init() {
        this.modelMap.set(Model.Forefront, new Forefrontnew(this.options))
    }

    get(model: Model): Chat | undefined {
        return this.modelMap.get(model);
    }
}
