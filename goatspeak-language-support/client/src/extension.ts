import * as path from 'path'
import { workspace, ExtensionContext } from 'vscode'
import {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions,
    TransportKind
} from 'vscode-languageclient/node'

export function activate(context: ExtensionContext) {
    const serverModule = context.asAbsolutePath(
        path.join('out', 'server', 'src', 'server.js')
    )

    const serverOptions: ServerOptions = {
        run: { module: serverModule, transport: TransportKind.ipc },
        debug: {
            module: serverModule,
            transport: TransportKind.ipc,
            options: { execArgv: ['--nolazy', '--inspect=6009'] }
        }
    }

    const clientOptions: LanguageClientOptions = {
        documentSelector: [{ scheme: 'file', language: 'goat' }],
        synchronize: {
            fileEvents: workspace.createFileSystemWatcher('**/.clientrc')
        }
    }

    const client = new LanguageClient(
        'goatLanguageServer',
        'Goat Language Server',
        serverOptions,
        clientOptions
    )

    client.start()
}

export function deactivate(): Thenable<void> | undefined {
    return undefined
}
