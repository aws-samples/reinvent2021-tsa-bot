const cdk = require('@aws-cdk/core');
const tsabot_service = require('../lib/tsabot_service');


class TSABotStack extends cdk.Stack {
  /**
   *
   * @param {cdk.Construct} scope
   * @param {string} id
   * @param {cdk.StackProps=} props
   */
  constructor(scope, id, props) {
    super(scope, id, props);

    // The code that defines your stack goes here
    new tsabot_service.tsaService(this, 'TSABot');
  }
}

module.exports = { TSABotStack }
