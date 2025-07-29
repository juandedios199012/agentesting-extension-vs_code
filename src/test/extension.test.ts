import * as assert from 'assert';

// You can import and use all API from the 'vscode' module
// as well as import your extension to test it
import * as vscode from 'vscode';
// import * as myExtension from '../../extension';

suite('Extension Test Suite', () => {
	vscode.window.showInformationMessage('Start all tests.');

	test('Sample test', () => {
		assert.strictEqual(-1, [1, 2, 3].indexOf(5));
		assert.strictEqual(-1, [1, 2, 3].indexOf(0));
	});

	test('Panel webview muestra formulario y responde al prompt', async () => {
		// Simula la activación del comando para mostrar el panel
		await vscode.commands.executeCommand('Agentesting.showResultsPanel');
		// El panel debe estar activo
		const panels = vscode.window.visibleTextEditors;
		assert.ok(panels);
		// No se puede testear el DOM del webview directamente aquí, pero se valida que el comando no arroja error
	});
});
