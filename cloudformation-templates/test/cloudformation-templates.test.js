const { expect, matchTemplate, MatchStyle } = require('@aws-cdk/assert');
const cdk = require('@aws-cdk/core');
const CloudformationTemplates = require('../lib/cloudformation-templates-stack');

test('Empty Stack', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new CloudformationTemplates.CloudformationTemplatesStack(app, 'MyTestStack');
    // THEN
    expect(stack).to(matchTemplate({
      "Resources": {}
    }, MatchStyle.EXACT))
});
