import { mount } from '@vue/test-utils';
import HelloWorld from '../HelloWorld.vue';

describe('HelloWorld.vue', () => {
  it('renders a greeting message', () => {
    const wrapper = mount(HelloWorld);
    expect(wrapper.text()).toContain('Hello World');
  });
});