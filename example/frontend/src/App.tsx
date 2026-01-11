import "./App.css";

import { request_with_args } from "./flask_urls/apis";
import { useState } from "react";

export default function App() {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const [endpointReturnValue, setEndpointReturnValue] = useState<any>(undefined);

    const requestEndpoint = () => {
        request_with_args({
            arg: false
        }).then(result => {
            setEndpointReturnValue(result);
        });
    }

    return (
        <div className="main">
            <h1>Typescript Flask URLs</h1>
            <div className="card">
                <button
                    onClick={requestEndpoint}
                >Make Request</button>
            </div>
            <p>
                Endpoint return:
            </p>
                <pre>
                    <code>
                        { JSON.stringify(endpointReturnValue) }
                    </code>
                </pre>
        </div>
    );
}
